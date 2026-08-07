If I were deploying your stack today, I'd choose **Oracle Cloud Free + Docker Compose**. It's one of the few free options that can run your existing architecture (PostgreSQL, Keycloak, Go API, and Next.js) with minimal changes.

---

# Architecture

You'll end up with something like this:

```text
Internet
       │
       ▼
+-----------------------------+
| Oracle Cloud Free VM        |
| Ubuntu 24.04               |
|                             |
| Docker                      |
| Docker Compose              |
|                             |
|  Next.js (3000)             |
|  API (8080)                 |
|  Keycloak (8180)            |
|  PostgreSQL (5432)          |
|                             |
| Caddy / Nginx               |
| HTTPS                       |
+-----------------------------+
```

You'll only expose ports **80 and 443** publicly. The other services stay private.

---

# Step 1. Create an Oracle Cloud Account

Go to:

**[Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/?utm_source=chatgpt.com)**

Create a Free Tier account.

Oracle will ask for:

* Credit card (verification only)
* Phone number
* Email

You are not charged unless you explicitly upgrade.

---

# Step 2. Create a VM

Open the Oracle Cloud Console.

Navigate to:

```
Compute
```

↓

```
Instances
```

↓

```
Create Instance
```

---

### Name

```
propertyhub
```

---

### Image

Choose

```
Ubuntu 24.04 LTS
```

---

### Shape

Click

```
Change Shape
```

Select

```
Ampere
```

Then choose:

```
4 OCPU

24 GB RAM
```

This is included in the Always Free limits.

---

### Networking

Leave defaults.

Oracle will create:

* Virtual Cloud Network (VCN)
* Public IP
* Subnet

---

### SSH Keys

Generate a new key pair or upload your own public key.

If generating one:

Download

```
id_rsa
```

and

```
id_rsa.pub
```

Keep the private key safe.

---

### Boot Volume

Default (around 50 GB) is fine.

Click **Create**.

Wait 2–5 minutes.

---

# Step 3. Connect via SSH

Find the public IP.

Example:

```
152.xxx.xxx.xxx
```

On macOS/Linux:

```bash
chmod 600 id_rsa

ssh -i id_rsa ubuntu@152.xxx.xxx.xxx
```

On Windows, you can use PowerShell/OpenSSH similarly.

---

# Step 4. Update Ubuntu

```bash
sudo apt update

sudo apt upgrade -y
```

---

# Step 5. Install Docker

```bash
curl -fsSL https://get.docker.com | sudo sh
```

Add your user to the Docker group:

```bash
sudo usermod -aG docker $USER
```

Log out and back in, or run:

```bash
newgrp docker
```

Verify:

```bash
docker --version
```

---

# Step 6. Install Docker Compose

Recent Docker versions include Compose.

Check:

```bash
docker compose version
```

If it returns a version, you're ready.

---

# Step 7. Install Git

```bash
sudo apt install git -y
```

---

# Step 8. Clone Your Repository

Example:

```bash
cd ~

git clone https://github.com/yourusername/propertyhub.git

cd propertyhub
```

---

# Step 9. Modify Your Compose File

Currently you expose every service:

```yaml
ports:
  - "5432:5432"
```

Don't expose internal services on the public internet.

Instead:

### PostgreSQL

Remove

```yaml
ports:
  - "5432:5432"
```

---

### Keycloak

Remove

```yaml
ports:
  - "8180:8180"
```

---

### API

Remove

```yaml
ports:
  - "8080:8080"
```

---

### Web

Only expose:

```yaml
ports:
  - "3000:3000"
```

Eventually, a reverse proxy (Caddy or Nginx) will expose ports 80/443 and forward traffic to port 3000.

---

# Step 10. Environment Variables

Create a production `.env` file.

Example:

```env
POSTGRES_USER=propertyhub

POSTGRES_PASSWORD=VeryStrongPassword

POSTGRES_DB=propertyhub

API_SECRET=GenerateSomethingRandom

KEYCLOAK_ADMIN=admin

KEYCLOAK_ADMIN_PASSWORD=AnotherStrongPassword

NEXT_PUBLIC_APP_URL=https://app.yourdomain.com

NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

Don't commit this file to Git.

---

# Step 11. Start Everything

```bash
docker compose up -d
```

Check:

```bash
docker ps
```

You should see:

```
postgres

keycloak

api

web
```

---

# Step 12. Verify Logs

```bash
docker compose logs -f
```

---

# Step 13. Buy a Domain (Optional but Recommended)

Examples:

* [Cloudflare Registrar](https://www.cloudflare.com/products/registrar/?utm_source=chatgpt.com)
* [Namecheap](https://www.namecheap.com?utm_source=chatgpt.com)

Suppose you buy:

```
propertyhub.app
```

Create DNS records:

```
app.propertyhub.app
```

↓

```
Your VM IP
```

And:

```
api.propertyhub.app
```

↓

```
Your VM IP
```

---

# Step 14. Install Caddy (Recommended)

Caddy automatically provisions and renews HTTPS certificates.

```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https

curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | \
sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg

curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | \
sudo tee /etc/apt/sources.list.d/caddy-stable.list

sudo apt update

sudo apt install caddy
```

Example `Caddyfile`:

```text
app.propertyhub.app {
    reverse_proxy localhost:3000
}

api.propertyhub.app {
    reverse_proxy localhost:8080
}

auth.propertyhub.app {
    reverse_proxy localhost:8180
}
```

Restart Caddy:

```bash
sudo systemctl reload caddy
```

Caddy will automatically obtain TLS certificates from Let's Encrypt once your DNS records point to the VM.

---

# Step 15. Open Firewall Ports

In the Oracle Cloud Console, update the VCN Security List or Network Security Group to allow inbound TCP on:

* 22 (SSH)
* 80 (HTTP)
* 443 (HTTPS)

You do **not** need to allow inbound 5432, 8080, or 8180 if those services are only accessed through Docker and Caddy.

---

# Step 16. Keep Containers Updated

To update your application after pushing new code:

```bash
git pull

docker compose build

docker compose up -d
```

To clean up unused images:

```bash
docker image prune -f
```

---

## Production Improvements

Before using this beyond a demo or sandbox, consider these changes:

* Use strong, unique passwords and secrets instead of development defaults.
* Set `restart: unless-stopped` (you already have this).
* Add regular backups for the PostgreSQL data volume.
* Configure Keycloak for production mode rather than `start-dev`.
* Use separate databases or schemas as appropriate (Keycloak typically benefits from its own database or at least a dedicated schema).
* Configure proper logging and monitoring.
* Set up automated deployments (for example, with GitHub Actions) if you plan to update frequently.

With those pieces in place, you'll have a free cloud environment that closely resembles a production deployment while still letting you keep your existing Docker Compose workflow.
