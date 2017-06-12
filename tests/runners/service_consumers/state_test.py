import requests
from pact_test import state
from pact_test import PactHelper
from pact_test import ServiceConsumerTest
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


def test_verify_state(mocker):
    class Response(object):
        status_code = 200
        headers = {'Content-Type': 'application/json'}

        def json(self):
            return {'spam': 'eggs'}

    mocker.patch.object(requests, 'request', lambda x, **kwargs: Response())

    test_instance = TestLibraryApp()
    pact_helper = MyPactHelper()

    mocker.spy(pact_helper, 'setup')
    mocker.spy(pact_helper, 'tear_down')

    response = verify_state(interaction, pact_helper, test_instance)

    assert pact_helper.setup.call_count == 1
    assert pact_helper.tear_down.call_count == 1
    assert pact_helper.tear_down.call_count == 1


interaction = {
    'providerState': 'some books exist',
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
        }
    }
}


class TestLibraryApp(ServiceConsumerTest):
    @state('some books exist')
    def test_get_book(self):
        pass
