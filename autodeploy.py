import os

if os.geteuid() != 0:
    print("Run with sudo!")
    exit()

domain = input("Enter domain name: ")
app_type = input("Type (proxy/php): ")

if app_type == "proxy":
    port = input("Enter app port: ")

    nginx_config = f"""
server {{
    listen 80;
    server_name {domain};

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

elif app_type == "php":
    path = input("Enter folder path (e.g. /var/www/adminer): ")

    nginx_config = f"""
server {{
    listen 80;
    server_name {domain};

    root {path};
    index index.php index.html;

    location / {{
        try_files $uri $uri/ =404;
    }}

    location ~ \\.php$ {{
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    }}
}}
"""

else:
    print("Invalid type")
    exit()

config_path = f"/etc/nginx/sites-available/{domain}"

with open(config_path, "w") as f:
    f.write(nginx_config)

print("Nginx config created")

os.system(f"ln -sf {config_path} /etc/nginx/sites-enabled/{domain}")
os.system("nginx -t")
os.system("systemctl reload nginx")

ssl = input("Install SSL with certbot? (y/n): ")

if ssl.lower() == "y":
    os.system(f"certbot --nginx -d {domain}")

print("Done!")
