import pytest

from main import create_app

resource_file = 'resources'


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        'TESTING': True
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_invalid_text_correction_requests(client):
    response = client.post('/correct-text', json={'id': '9f69b23b-65b0-48e0-b688-4e3bf2b01bb5'})
    assert 400 == response.status_code
    response = client.post('/correct-text', json={'text': 'text correction'})
    assert 400 == response.status_code
    response = client.post('/correct-text', json={})
    assert 400 == response.status_code


def test_valid_text_correction_request(client):
    response = client.post('/correct-text', json={'id': '9f69b23b-65b0-48e0-b688-4e3bf2b01bb5', 'text': 'text'})
    assert 202 == response.status_code


def test_read_request_with_no_image(client):
    response = client.post('/read', data={}, content_type='multipart/form-data')
    assert 400 == response.status_code


def test_read_request_with_image_too_large(client):
    with open(f'{resource_file}/image_too_large.jpg', 'rb') as image:
        data = {'image': image}
        response = client.post('/read', data=data, content_type='multipart/form-data')
        assert 400 == response.status_code


def test_read_request_with_image_size_ok(client):
    with open(f'{resource_file}/image_ok_dim.jpg', 'rb') as image:
        data = {'image': image}
        response = client.post('/read', data=data, content_type='multipart/form-data')
        assert 200 == response.status_code
        assert 'id' in response.json and 'text' in response.json
