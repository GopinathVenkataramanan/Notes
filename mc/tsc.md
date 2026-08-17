Yes. The main change is that you should **stop doing the Cosmos lookup inside the loop**. Instead:

1. Build one array of all SNOMED codes.
2. Run **one Cosmos DB query** using `ARRAY_CONTAINS`.
3. Return all matching `{ code, description, snomedCode }` records.
4. In your Logic Apps JavaScript, map those results back to the original `readCodes`.
5. Preserve your existing behaviour for:

   * no match
   * one READ code match
   * multiple READ code matches
   * primary vs secondary codes
   * `canAutomate`
   * warning messages.

Cosmos DB supports parameterized queries where the parameter value can itself be an array, and `ARRAY_CONTAINS` can test each document's SNOMED code against that array. ([Microsoft Learn][1])

## 1. Cosmos DB query

Assuming your Cosmos documents look something like:

```json
{
  "SNOMED_CODE": "123456789",
  "READ_CODE": "E11..",
  "READ_CODE_DESC": "Type 2 diabetes mellitus"
}
```

use:

```sql
SELECT
    c.READ_CODE AS code,
    c.READ_CODE_DESC AS description,
    c.SNOMED_CODE AS snomedCode
FROM c
WHERE ARRAY_CONTAINS(@snomedCodes, c.SNOMED_CODE)
```

For example, your parameter would be:

```json
{
  "name": "@snomedCodes",
  "value": [
    "123456789",
    "987654321",
    "555555555"
  ]
}
```

This gives you all matching mappings in **one query**, rather than:

```text
SNOMED 1 -> Cosmos query
SNOMED 2 -> Cosmos query
SNOMED 3 -> Cosmos query
SNOMED 4 -> Cosmos query
...
```

Instead:

```text
SNOMED 1 ┐
SNOMED 2 ├──> ONE Cosmos query ──> all mappings
SNOMED 3 │
SNOMED 4 ┘
```

The Logic Apps Cosmos DB connector has a **Query items** operation for executing Cosmos SQL. ([Microsoft Learn][2])

---

# 2. Build the SNOMED array before the Cosmos query

Your existing `tw.local.readCodes` appears to contain something like:

```text
readCodes
    snomedCode
    isPrimary
    readCodeFound
    multipleReadCodesFound
    code
    description
    multipleReadCodes
```

Before calling Cosmos, extract all the SNOMED codes.

For an Azure Logic Apps JavaScript Code action, you can do:

```javascript
var snomedCodes = [];

for (var i = 0; i < readCodes.length; i++) {
    var snomedCode = readCodes[i].snomedCode;

    if (snomedCode !== null &&
        snomedCode !== undefined &&
        snomedCode !== "") {

        if (snomedCodes.indexOf(snomedCode) === -1) {
            snomedCodes.push(snomedCode);
        }
    }
}

return snomedCodes;
```

I would recommend removing duplicates because there is no benefit in sending the same SNOMED code multiple times.

---

# 3. Cosmos result

The Cosmos query should return something like:

```json
[
  {
    "code": "E11..",
    "description": "Type 2 diabetes mellitus",
    "snomedCode": "123456789"
  },
  {
    "code": "E11.9",
    "description": "Type 2 diabetes mellitus without complication",
    "snomedCode": "123456789"
  },
  {
    "code": "J45..",
    "description": "Asthma",
    "snomedCode": "987654321"
  }
]
```

This is important because your old Oracle query was:

```sql
select READ_CODE as code,
       READ_CODE_DESC as description
from SNOMED_READCODE_MAPPING
where SNOMED_CODE=?
```

When you're querying **multiple SNOMED codes**, I strongly recommend returning `SNOMED_CODE` as well.

Otherwise, after Cosmos returns the records, you have no reliable way to know which SNOMED code each READ code belongs to.

So use:

```sql
SELECT
    c.READ_CODE AS code,
    c.READ_CODE_DESC AS description,
    c.SNOMED_CODE AS snomedCode
FROM c
WHERE ARRAY_CONTAINS(@snomedCodes, c.SNOMED_CODE)
```

---

# 4. Replace your child-flow mapping logic

Your current child-flow code:

```javascript
tw.local.multipleReadCodesFound = false;
tw.local.isReadCodeFound = false;
tw.local.multipleReadCodes = new tw.object.listOf.NameValuePair();
tw.local.readCode = "";
tw.local.readCodeDescription = "";
```

is essentially doing the mapping **one SNOMED code at a time**.

After the Cosmos query, you can instead process the complete result set.

For example, assuming:

```javascript
readCodes
```

is your input array and:

```javascript
cosmosResults
```

is the result from Cosmos:

```javascript
var results = [];

if (cosmosResults) {
    results = cosmosResults;
}

for (var i = 0; i < readCodes.length; i++) {

    var current = readCodes[i];

    // Reset mapping information
    current.readCodeFound = false;
    current.multipleReadCodesFound = false;
    current.code = "";
    current.description = "";
    current.multipleReadCodes = [];

    if (!current.snomedCode) {
        continue;
    }

    // Find all READ code mappings for this SNOMED code
    var matches = [];

    for (var j = 0; j < results.length; j++) {

        if (results[j].snomedCode == current.snomedCode) {
            matches.push(results[j]);
        }
    }

    // No READ code found
    if (matches.length === 0) {

        current.readCodeFound = false;
        current.multipleReadCodesFound = false;

    // Exactly one READ code found
    } else if (matches.length === 1) {

        current.readCodeFound = true;
        current.multipleReadCodesFound = false;

        current.code = matches[0].code;

        if (matches[0].description) {
            current.description = matches[0].description;
        }

    // Multiple READ codes found
    } else {

        current.readCodeFound = true;
        current.multipleReadCodesFound = true;

        for (var k = 0; k < matches.length; k++) {

            current.multipleReadCodes.push({
                value: matches[k].code,
                name: matches[k].description
            });
        }
    }
}

return readCodes;
```

That is the direct conceptual replacement for your BAW child-flow code.

---

# 5. But I would make one improvement

The code above searches the Cosmos results repeatedly:

```javascript
for each readCode
    for each cosmosResult
```

That is okay for a small number of codes, but you can make it cleaner by building a lookup map once.

For example:

```javascript
var mappingBySnomed = {};

for (var i = 0; i < cosmosResults.length; i++) {

    var result = cosmosResults[i];

    if (!result.snomedCode) {
        continue;
    }

    if (!mappingBySnomed[result.snomedCode]) {
        mappingBySnomed[result.snomedCode] = [];
    }

    mappingBySnomed[result.snomedCode].push(result);
}
```

Then process `readCodes`:

```javascript
for (var i = 0; i < readCodes.length; i++) {

    var current = readCodes[i];

    current.readCodeFound = false;
    current.multipleReadCodesFound = false;
    current.code = "";
    current.description = "";
    current.multipleReadCodes = [];

    if (!current.snomedCode) {
        continue;
    }

    var matches = mappingBySnomed[current.snomedCode];

    if (!matches || matches.length === 0) {

        // No match
        current.readCodeFound = false;

    } else if (matches.length === 1) {

        // One match
        current.readCodeFound = true;
        current.multipleReadCodesFound = false;
        current.code = matches[0].code;
        current.description = matches[0].description || "";

    } else {

        // Multiple matches
        current.readCodeFound = true;
        current.multipleReadCodesFound = true;

        for (var j = 0; j < matches.length; j++) {

            current.multipleReadCodes.push({
                value: matches[j].code,
                name: matches[j].description || ""
            });
        }
    }
}

return readCodes;
```

I would use **this version**.

---

# 6. Then your calling Logic App script

The nice thing is that most of your existing calling logic can remain conceptually the same.

You no longer need:

```javascript
tw.local.
```

So this:

```javascript
tw.local.readCodes
```

becomes:

```javascript
readCodes
```

And this:

```javascript
tw.local.readCodes[i].readCodeFound
```

becomes:

```javascript
readCodes[i].readCodeFound
```

Your primary-code validation can therefore become:

```javascript
var matchForPrimary = true;
var matchForSecondary = true;
var canAutomate = true;
var status = "SNOMED to READ Code Match Successful";
var msgList = [];

function AddMsgData(id, type, title, message) {

    msgList.push({
        id: id,
        type: type,
        title: title,
        message: message
    });
}

for (var i = 0; i < readCodes.length; i++) {

    if (readCodes[i].isPrimary === true &&
        readCodes[i].readCodeFound === false) {

        matchForPrimary = false;
        canAutomate = false;

        status = "matchingReadCodeNotFound";

        AddMsgData(
            "WCMC_SNOMED",
            snomedType,
            snomedTitle,
            noReadCodeFoundMessage
        );

        break;
    }
}
```

---

# 7. Your multiple READ code logic

This part can also be converted almost directly.

For a clinical condition:

```javascript
for (var i = 0; i < readCodes.length; i++) {

    var snomed = readCodes[i];

    if (!snomed.readCodeFound) {
        continue;
    }

    if (!medCert.clinicalCondition) {
        continue;
    }

    for (var j = 0; j < medCert.clinicalCondition.length; j++) {

        var condition = medCert.clinicalCondition[j];

        if (!condition.readcode) {
            continue;
        }

        if (condition.readcode.indexOf(snomed.snomedCode) === -1) {
            continue;
        }

        // Multiple READ codes + Primary SNOMED
        if (snomed.multipleReadCodesFound === true &&
            snomed.isPrimary === true) {

            canAutomate = false;
            status = "multipleReadCodeFound";

            var msg =
                multipleReadCodesMessage +
                snomed.snomedCode +
                " - " +
                condition.description +
                " :-";

            AddMsgData(
                "WCMC_SNOMED",
                snomedType,
                snomedTitle,
                msg
            );

            var multiReadCodes = snomed.multipleReadCodes;

            for (var k = 0; k < multiReadCodes.length; k++) {

                msg =
                    (k + 1) +
                    ". " +
                    multiReadCodes[k].value +
                    " - " +
                    multiReadCodes[k].name;

                AddMsgData(
                    "WCMC_SNOMED",
                    snomedType,
                    snomedTitle,
                    msg
                );
            }

        // Exactly one READ code
        } else if (snomed.multipleReadCodesFound === false) {

            condition.readcode = snomed.code;

            if (snomed.description) {
                condition.description = snomed.description;
            }
        }
    }
}
```

---

# 8. One important issue in your existing code

You currently have:

```javascript
medCert.clinicalCondition[j].readcode.match(
    tw.local.readCodes[i].snomedCode
)
```

I would **not blindly carry that over** to JavaScript.

`match()` treats its argument as a regular expression when used with a string. If your SNOMED code contains characters that have regex meaning, that can produce unexpected results.

If you're looking for a simple substring match, use:

```javascript
condition.readcode.indexOf(snomed.snomedCode) !== -1
```

Or, if the field should be an exact SNOMED code, use:

```javascript
condition.readcode === snomed.snomedCode
```

The latter is preferable if your data model allows it.

---

# 9. Recommended overall Logic App design

I would restructure your Logic App/child flow approximately like this:

```text
                    ┌─────────────────────────┐
                    │ Input readCodes         │
                    │                         │
                    │ SNOMED 1                │
                    │ SNOMED 2                │
                    │ SNOMED 3                │
                    │ SNOMED 4                │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ JavaScript              │
                    │                         │
                    │ Extract SNOMED codes    │
                    │ Remove duplicates       │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ Cosmos DB Query         │
                    │                         │
                    │ ARRAY_CONTAINS(         │
                    │   @snomedCodes,         │
                    │   c.SNOMED_CODE         │
                    │ )                       │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ JavaScript              │
                    │                         │
                    │ Group results by        │
                    │ snomedCode              │
                    │                         │
                    │ 1 match  -> code       │
                    │ >1       -> multiple   │
                    │ 0        -> not found  │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ Calling Script          │
                    │                         │
                    │ Primary validation      │
                    │ Clinical conditions     │
                    │ Pregnancy conditions    │
                    │ Messages                │
                    │ canAutomate             │
                    └─────────────────────────┘
```

This removes the expensive pattern you currently have:

```text
Loop
  ↓
Child flow
  ↓
Cosmos query
  ↓
Return
  ↓
Loop
  ↓
Child flow
  ↓
Cosmos query
```

and replaces it with:

```text
Extract all SNOMED codes
        ↓
ONE Cosmos query
        ↓
Map all results
        ↓
Continue processing
```

---

## 10. One more Cosmos consideration: partition key

There is one important performance consideration I would check before implementing this.

If `SNOMED_CODE` is your **Cosmos partition key**, you may want to pass the partition key appropriately. If it isn't the partition key, the `ARRAY_CONTAINS` query may become a cross-partition query depending on your container configuration.

The Cosmos Logic Apps connector exposes a **Partition Key** option for its query operation. ([Microsoft Learn][2])

Also, `ARRAY_CONTAINS` can benefit from a range index, according to Microsoft's Cosmos DB documentation. ([Microsoft Learn][3])

### My recommended query

```sql
SELECT
    c.READ_CODE AS code,
    c.READ_CODE_DESC AS description,
    c.SNOMED_CODE AS snomedCode
FROM c
WHERE ARRAY_CONTAINS(@snomedCodes, c.SNOMED_CODE)
```

### And the important architectural change

**Don't try to reproduce the old BAW loop in Logic Apps.** The whole point of the Cosmos migration is to let Cosmos return all mappings in one operation, then use JavaScript to group those results by `snomedCode`.

If you show me the **actual JSON structure of your `readCodes` input and one sample Cosmos document**, I can convert your two BAW scripts into **one complete Azure Logic Apps JavaScript Code action**, including the exact `canAutomate`, `status`, `UserMessage`, `clinicalCondition`, and `pregnancyCondition` handling.

[1]: https://learn.microsoft.com/en-us/cosmos-db/query/parameterized-queries?utm_source=chatgpt.com "Parameterized Queries - Query Language for Cosmos DB (in Azure and Fabric) | Microsoft Learn"
[2]: https://learn.microsoft.com/en-us/azure/logic-apps/connectors/built-in/reference/azurecosmosdb/?utm_source=chatgpt.com "Azure Cosmos DB - Connectors | Microsoft Learn"
[3]: https://learn.microsoft.com/en-us/cosmos-db/query/array-contains?utm_source=chatgpt.com "ARRAY_CONTAINS - Query Language for Cosmos DB (in Azure and Fabric) | Microsoft Learn"
