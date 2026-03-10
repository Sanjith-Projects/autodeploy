import os

domain = input("Enter domain name: ")
port = input("Enter app port: ")

nginx_config = f"""
server {{
    listen 80;
    server_name {domain} www.{domain};

    location / {{
        proxy_pass http://127.0.0.1:{port};
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }}
}}
"""

config_path = f"/etc/nginx/sites-available/{domain}"

with open(config_path, "w") as f:
    f.write(nginx_config)

print("Nginx config created")

os.system(f"ln -s {config_path} /etc/nginx/sites-enabled/{domain}")

os.system("nginx -t")

os.system("systemctl reload nginx")

ssl = input("Install SSL with certbot? (y/n): ")

if ssl.lower() == "y":
    os.system(f"certbot --nginx -d {domain} -d www.{domain}")

print("Done!")