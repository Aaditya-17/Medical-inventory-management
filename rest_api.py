import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import oracledb
from datetime import date, datetime
from decimal import Decimal

DB_CONFIG = {
    "user": "system",         # Oracle database username
    "password": "root",     # Oracle database password
    "dsn": "localhost:1521/XE"  
}

def get_db_connection():
    return oracledb.connect(**DB_CONFIG)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()  # Convert to ISO 8601 string
        if isinstance(obj, Decimal):
            return float(obj)  # Convert Decimal to float
        return super().default(obj)

# HTTP Request Handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.rowfactory = lambda *args: dict(zip([d[0].lower() for d in cursor.description], args))

            if self.path.startswith("/medicines/"):
                medicine_id = self.path.split("/")[-1]
                query = "SELECT * FROM medicines WHERE medicineid = :1"
                cursor.execute(query, [medicine_id])
                result = cursor.fetchone()
            else:
                query = "SELECT * FROM medicines"
                cursor.execute(query)
                result = cursor.fetchall()

            response_body = json.dumps(result, cls=CustomJSONEncoder)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(response_body.encode())
        except Exception as e:
            self.send_error(500, str(e))
        finally:
            cursor.close()
            conn.close()

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            # Extract data from the JSON payload
            medicine_id = data['MedicineID']
            medicine_name = data['MedicineName']
            category = data.get('Category', None)  # Optional field
            unit_price = data['UnitPrice']

            conn = get_db_connection()
            cursor = conn.cursor()

            # SQL query to insert a new medicine
            query = """
                INSERT INTO Medicines (MedicineID, MedicineName, Category, UnitPrice)
                VALUES (:1, :2, :3, :4)
            """
            cursor.execute(query, [medicine_id, medicine_name, category, unit_price])
            conn.commit()

            # Send success response
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response_body = json.dumps({"message": "Medicine added successfully"})
            self.wfile.write(response_body.encode())
        except Exception as e:
            self.send_error(500, str(e))
        finally:
            cursor.close()
            conn.close()

    def do_DELETE(self):
        conn = None
        cursor = None
        try:
            if self.path.startswith("/medicines/"):
                medicine_id = self.path.split("/")[-1]
                conn = get_db_connection()
                cursor = conn.cursor()
                query_check = (f"SELECT COUNT(*) FROM Medicines WHERE MedicineID ={medicine_id}")
                cursor.execute(query_check)
                count = cursor.fetchone()[0]

                if count == 0:
                    self.send_error(404, "Medicine not found")
                    return
                query_delete = (f"DELETE FROM Medicines WHERE MedicineID = {medicine_id}")
                cursor.execute(query_delete)
                conn.commit()
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                response_body = json.dumps({"message": "Medicine deleted successfully"})
                self.wfile.write(response_body.encode())
            else:
                self.send_error(400, "Invalid endpoint")
        except Exception as e:
            self.send_error(500, str(e))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def do_PUT(self):
        conn = None
        cursor = None
        try:
            if self.path.startswith("/medicines/"):
                medicine_id = self.path.split("/")[-1]
                content_length = int(self.headers['Content-Length'])
                put_data = self.rfile.read(content_length)
                data = json.loads(put_data)
                medicine_name = data.get("MedicineName")
                category = data.get("Category")
                unit_price = data.get("UnitPrice")
                conn = get_db_connection()
                cursor = conn.cursor()
                query_check = "SELECT COUNT(*) FROM Medicines WHERE MedicineID = :1"
                cursor.execute(query_check, [medicine_id])
                count = cursor.fetchone()[0]

                if count == 0:
                    self.send_error(404, "Medicine not found")
                    return
                updates = []
                params = []

                if medicine_name:
                    updates.append("MedicineName = :1")
                    params.append(medicine_name)
                if category:
                    updates.append("Category = :2")
                    params.append(category)
                if unit_price is not None:
                    updates.append("UnitPrice = :3")
                    params.append(unit_price)

                params.append(medicine_id)
                query_update = f"UPDATE Medicines SET {', '.join(updates)} WHERE MedicineID = :4"
                cursor.execute(query_update, params)
                conn.commit()
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                response_body = json.dumps({"message": "Medicine updated successfully"})
                self.wfile.write(response_body.encode())
            else:
                self.send_error(400, "Invalid endpoint")
        except Exception as e:
            self.send_error(500, str(e))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

# Server Runner
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
