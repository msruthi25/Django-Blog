import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_register_view(client):
    url = reverse("createUser")  
    data = {
        "username": "newuser",
        "email": "newuser@gmail.com",  
        "password": "newpass123"
        
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse("login") 
    
@pytest.mark.django_db
def test_login_view(client, test_user):
    url = reverse("login")
    data = {
        "username": test_user.username,
        "password": "testpass123"
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse("posts") 


@pytest.mark.django_db
def test_logout_view(client, test_user):
    # First login the user
    client.login(username=test_user.username, password="testpass123")
    url = reverse("logout")
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse("posts")     