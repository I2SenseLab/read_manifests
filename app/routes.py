from flask import Blueprint, render_template
from app.get_records import enumerate_and_get_dns_records,load_manifest_data
import os
main = Blueprint('main', __name__)

# Sample DNS records (replace with your actual records)
dns_records = enumerate_and_get_dns_records(os.getenv('DOMAIN', 'fl2f.ca'))
subdomain_data = load_manifest_data(dns_records)
@main.route('/')
def index():
    return render_template('index.html', dns_records=dns_records, subdomain_data=subdomain_data)
