
# Ecommerce Backend

An ecommerce site backend written in django with razorpay integration


## Features

- User Authentication (Social Authentication in development)
- Vendor Model
- Vendor Dashboard
- Functional Cart System
- Order Accepting
- Flexible Payment Integration (Razor Pay Integrated)


## Run Locally

Clone the project

```bash
  git clone https://github.com/DivyanshuLohani/EcommerceBackend
```

Go to the project directory

```bash
  cd EcommerceBackend
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python3 ./manage.py runserver
```




## API Reference

### Authentication
Authentication is handled by a library known as djoser you can visit the documentation [here](https://djoser.readthedocs.io/)

### Addresses

#### Create Address
```http
  POST /auth/addresses/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `name`      | `string` | **Required**. Billing name |
| `contact`      | `string` | **Required**. Billing Contact |
| `postal_code`      | `string` | **Required**. Postal Code |
| `flat_name`      | `string` | Appartment, Building, House No |
| `area`      | `string` | **Required**. Street or full address |
| `landmark`      | `string` | Lankmark |
| `city`      | `string` | **Required.** City |
| `Country`      | `string` | **Required.** Country |
| `Default`      | `bool` | Weather this will be Default address |

```json
{
  "created_at": "2023-12-25T09:09:23.596636Z",
  "updated_at": "2023-12-25T09:09:23.596636Z",
  "uid": "eBM2wsNoZVC7fisvWhGuVR",
  "name": "Ryan",
  "contact": "3578964523",
  "postal_code": "123456",
  "flat_name": "",
  "area": "Area",
  "landmark": "",
  "city": "City",
  "country": "India",
  "default": false
}
```

#### Get Address 
```http
  POST /address/<uid>/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `uid`      | `string` | **Required**. Address ID returned by the server |

```json
{
  "created_at": "2023-12-25T09:09:23.596636Z",
  "updated_at": "2023-12-25T09:09:23.596636Z",
  "uid": "eBM2wsNoZVC7fisvWhGuVR",
  "name": "Ryan",
  "contact": "3578964523",
  "postal_code": "123456",
  "flat_name": "",
  "area": "Area",
  "landmark": "",
  "city": "City",
  "country": "India",
  "default": false
}
```

