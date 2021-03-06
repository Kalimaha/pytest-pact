import requests
from pact_test import state
from pact_test import PactHelper
from pact_test import ServiceConsumerTest
from pact_test.runners.service_consumers.state_test import find_state
from pact_test.runners.service_consumers.state_test import verify_state


class MyPactHelper(PactHelper):
    def setup(self):
        pass

    def tear_down(self):
        pass


class TestLibraryApp(ServiceConsumerTest):
    @state('some books exist')
    def test_get_book(self):
        pass

test_instance = TestLibraryApp()
pact_helper = MyPactHelper()


def test_find_state():
    response = find_state(interaction, '', test_instance).value
    assert type(response).__name__.endswith('method')


def test_missing_state():
    i = interaction.copy()
    i['providerState'] = 'Catch me if you can'

    test_instance = TestLibraryApp()
    pact_helper = MyPactHelper()

    response = verify_state(i, pact_helper, test_instance).value
    expected_response = {
        'state': 'Catch me if you can',
        'description': 'Description',
        'status': 'FAILED',
        'errors': ['Missing state implementation for "Catch me if you can"']
    }

    assert response == expected_response


def test_find_state_missing():
    class BadTest(ServiceConsumerTest):
        pass

    bad_test_instance = BadTest()
    expected_response = {
        'state': 'some books exist',
        'description': 'Description',
        'status': 'FAILED',
        'errors': [
            'Missing state implementation for "some books exist"'
        ]
    }
    response = find_state(interaction, 'Description', bad_test_instance).value
    assert response == expected_response


def test_verify_state(mocker):
    class Response(object):
        status_code = 200
        headers = {'Content-Type': 'application/json'}

        def json(self):
            return {
                'id': 42,
                'title': 'The Hitchhicker\'s Guide to the Galaxy'
            }

    mocker.patch.object(requests, 'request', lambda x, **kwargs: Response())

    test_instance = TestLibraryApp()
    pact_helper = MyPactHelper()

    mocker.spy(pact_helper, 'setup')
    mocker.spy(pact_helper, 'tear_down')

    response = verify_state(interaction, pact_helper, test_instance).value
    expected_response = {
        'state': 'some books exist',
        'description': 'Description',
        'status': 'PASSED',
        'errors': []
    }

    assert response == expected_response


interaction = {
    'providerState': 'some books exist',
    'description': 'Description',
    'request': {
        'method': 'GET',
        'path': '',
        'query': '',
        'headers': {
            'Content-type': 'application/json'
        },
        'body': {
            'title': 'The Hitchhicker\'s Guide to the Galaxy'
        }
    },
    'response': {
        'status': 200,
        'body': {
            'id': 42,
            'title': 'The Hitchhicker\'s Guide to the Galaxy'
        },
        'headers': {
            'Content-Type': 'application/json'
        }
    }
}


class TestLibraryApp(ServiceConsumerTest):
    @state('some books exist')
    def test_get_book(self):
        pass

    @state('no books exist')
    def test_no_book(self):
        pass
