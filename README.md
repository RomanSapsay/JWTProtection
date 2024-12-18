
## JWT

### 1. Login with token

**Methon**: `POST`  
**Path**: `/login`

**Body**:
```json
{
    "username": "admin",
    "password": "adminpassword"
}
```

**Responce**:
```json
{
    "access_token": "your-jwt-token"
}
```


