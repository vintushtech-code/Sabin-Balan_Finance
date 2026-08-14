import sqlite3
import logging
from django.apps import AppConfig
from django.conf import settings

logger = logging.getLogger(__name__)


class LoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'login'
    verbose_name = 'Standalone Authentication & User Management'

    def ready(self):
        """
        Auto-applies schema migration for ConsultationBooking dynamic billing & pricing fields.
        Ensures smooth zero-downtime execution without requiring manual command-line migration execution.
        """
        try:
            db_path = settings.BASE_DIR / 'db.sqlite3'
            if db_path.exists():
                conn = sqlite3.connect(str(db_path))
                cursor = conn.cursor()
                
                # Check existing columns in login_consultationbooking table
                cursor.execute("PRAGMA table_info(login_consultationbooking)")
                existing_cols = [row[1] for row in cursor.fetchall()]
                
                if existing_cols:
                    columns_to_add = [
                        ("fee_amount", "decimal DEFAULT 5000.0"),
                        ("discount_amount", "decimal DEFAULT 0.0"),
                        ("net_amount", "decimal DEFAULT 5000.0"),
                        ("invoice_number", "varchar(50) DEFAULT ''"),
                        ("payment_method", "varchar(50) DEFAULT 'UPI / Net Banking / Card'"),
                        ("transaction_id", "varchar(100) DEFAULT ''"),
                        ("fiduciary_desk", "varchar(150) DEFAULT 'Senior Wealth Advisory & Fiduciary Desk'"),
                        ("meeting_link", "varchar(500) DEFAULT ''"),
                        ("client_instructions", "text DEFAULT ''"),
                    ]
                    for col_name, col_type in columns_to_add:
                        if col_name not in existing_cols:
                            cursor.execute(f"ALTER TABLE login_consultationbooking ADD COLUMN {col_name} {col_type}")
                    
                    # Ensure migration record is registered in django_migrations
                    cursor.execute("SELECT name FROM django_migrations WHERE app='login' AND name='0010_consultationbooking_billing_fields'")
                    if not cursor.fetchone():
                        import datetime
                        cursor.execute(
                            "INSERT INTO django_migrations (app, name, applied) VALUES (?, ?, ?)",
                            ('login', '0010_consultationbooking_billing_fields', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        )
                    conn.commit()
                conn.close()
        except Exception as e:
            logger.warning("[LoginConfig] Auto-migration check: %s", e)
