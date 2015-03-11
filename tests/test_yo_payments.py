#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
import unittest
from mock import Mock, MagicMock

import responses

from yo_payments import YoClient, Yo
import yo_payments


STATUS = "Status"

RESPONSE = "Response"

AUTO_CREATE = "AutoCreate"

CONTENT_TYPE = "Content-Type"


class CustomTestCase(TestCase):
    def setUp(self):
        self.username = "username"
        self.password = "password"
        self.url = "https://paymentsapi1.yo.co.ug/ybs/task.php"

    def create_test_client(self):
        client = YoClient(self.username, self.password, self.url)
        return client

    def setup_response(self, content):
        responses.add(responses.POST, self.url,
                      body=content, status=200,
                      content_type='application/json')

    def setup_ok_response(self):
        self.setup_response("""
        <AutoCreate>
   <Response>
      <Status>OK</Status>
      <StatusCode>0</StatusCode>
   </Response>
</AutoCreate>
        """)


class TestYoClient(CustomTestCase):
    def test_that_content_type_is_xml(self):
        client = self.create_test_client()
        headers = client.get_headers()
        self.assertTrue(CONTENT_TYPE in headers.keys())
        self.assertEqual(headers[CONTENT_TYPE], "text/xml")

    def test_xml_data_should_contain_username(self):
        client = self.create_test_client()
        xml_data = client.get_xml_data("method", {})
        self.assertTrue("<APIUsername>username</APIUsername>" in xml_data)

    def test_xml_data_should_contain_password(self):
        client = self.create_test_client()
        xml_data = client.get_xml_data("method", {})
        self.assertTrue("<APIPassword>password</APIPassword>" in xml_data)

    def test_xml_data_should_contain_method(self):
        client = self.create_test_client()
        xml_data = client.get_xml_data("method", {})
        self.assertTrue("<Method>method</Method>" in xml_data)

    def test_xml_data_should_contain_extra_xml_if_available(self):
        client = self.create_test_client()
        xml_data = client.get_xml_data("method", {"name": "james"})
        self.assertTrue("<name>james</name>" in xml_data)

    def test_should_parse_the_xml_result_to_dict(self):
        client = self.create_test_client()
        content = """<?xml version="1.0" encoding="UTF-8"?>
<AutoCreate>
   <Response>
      <Status>OK</Status>
      <StatusCode>0</StatusCode>
      <TransactionStatus>SUCCEEDED</TransactionStatus>
      <TransactionReference></TransactionReference>
      <MNOTransactionReferenceId></MNOTransactionReferenceId>
   </Response>
</AutoCreate>
        """
        fake_response = Mock()
        fake_response.text = content
        data = client.parse_xml_response_to_dict(fake_response)
        self.assertTrue(AUTO_CREATE in data)
        self.assertTrue(RESPONSE in data[AUTO_CREATE])
        self.assertTrue(STATUS in data[AUTO_CREATE][RESPONSE])
        self.assertTrue("OK" == data[AUTO_CREATE][RESPONSE][STATUS])

    @responses.activate
    def test_response_should_have_status_message(self):
        client = self.create_test_client()
        self.setup_ok_response()
        response = client.make_request("method")
        self.assertTrue(response.is_ok())


class YoTestCase(CustomTestCase):
    @responses.activate
    def test_withdraw_funds_requires_a_valid_account(self):
        self.setup_ok_response()
        with self.assertRaises(Exception):
            yo = Yo("username", "password")
            yo.withdraw_funds(200, "+123", "for some reason")

    @responses.activate
    def test_should_setup_internal_reference_if_set(self):
        self.setup_ok_response()
        yo = Yo("username", "password")
        mock = MagicMock()
        yo.client = mock
        reference = "some reference"
        reason = "for some reason"
        Account = "123"
        yo.withdraw_funds(200, Account, reason, internal_reference=reference)
        yo.client.make_request.assert_called_with(self.get_method(),
                                                  Amount=200,
                                                  InternalReference=reference,
                                                  Account=Account,
                                                  NonBlocking='FALSE',
                                                  Narrative=reason)

    @responses.activate
    def test_should_setup_external_reference_if_set(self):
        self.setup_ok_response()
        yo = Yo("username", "password")
        mock = MagicMock()
        yo.client = mock
        reference = "some reference"
        reason = "for some reason"
        Account = "123"
        yo.withdraw_funds(200, Account, reason, external_reference=reference)
        yo.client.make_request.assert_called_with(self.get_method(),
                                                  Amount=200,
                                                  ExternalReference=reference,
                                                  Account=Account,
                                                  NonBlocking='FALSE',
                                                  Narrative=reason)

    def get_method(self):
        return yo_payments.ACDEPOSITFUNDS

    @responses.activate
    def test_should_setup_provider_reference_text_if_set(self):
        self.setup_ok_response()
        yo = Yo("username", "password")
        mock = MagicMock()
        yo.client = mock
        ref = "some reference"
        reason = "for some reason"
        account = "123"
        yo.withdraw_funds(200, account, reason,
                          provider_reference_text=ref)
        yo.client.make_request.assert_called_with(self.get_method(),
                                                  Amount=200,
                                                  ProviderReferenceText=ref,
                                                  Account=account,
                                                  NonBlocking='FALSE',
                                                  Narrative=reason)

    if __name__ == '__main__':
        unittest.main()
