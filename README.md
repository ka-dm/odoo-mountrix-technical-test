# odoo-mountrix-technical-test

## Requirements

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/odoo-mountrix-technical-test.git
   cd odoo-mountrix-technical-test
   ```

2. **Start the services:**
   ```bash
   docker-compose up
   ```
   This will start Odoo and the required PostgreSQL database.

3. **Access Odoo:**
   - Open your browser and go to: [http://localhost:8069](http://localhost:8069)

4. **Login:**
   - The default database and admin credentials will depend on your `docker-compose.yml` and `odoo.conf` settings. If not set, you will be prompted to create a new database on first access.

5. **Custom Addons:**
   - The custom module `purchase_rfq_comparator` is located in `extra-addons/`.
   - Make sure to add `extra-addons` to your Odoo addons path if not already configured.

## Stopping the Services

To stop the containers, press `Ctrl+C` in the terminal where Docker Compose is running, or run:
```bash
docker-compose down
```

## Notes

- Data is persisted in the `odoo-db-data/` and `odoo-web-data/` directories.
- For development, you can modify the code in `extra-addons/purchase_rfq_comparator/` and restart the Odoo service.

---

Feel free to update this README with more details about your modules, configuration, or usage instructions!