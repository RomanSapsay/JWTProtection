## Requirements
- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Smorest
- Marshmallow

## Installation
### 1. Clone repo
```bash
git clone 'insert repo url'
cd flask-api
```
### 2. Vm
```bash
python -m venv venv
```
```bash
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Run app
```bash
flask run
```

### **#API server http://127.0.0.1:5000/.**

## API Endpoints
### Store
- **GET** `/stores` - Get list of all stores
- **GET** `/stores/<int:store_id>` - Get specific store by ID
- **POST** `/stores` - Create new store 
- **DELETE** `/stores/<int:store_id>` - Delete store by ID
### Items
- **GET** `/item/<int:item_id>` - Get specific items by ID
- **POST** `/item` - Create new item
- **DELETE** `/item/<int:item_id>` - Delete item by ID


