SAML authentication in Building Bridges
=============

Building bridges can be hosted behind SAML, meaning, that people which are not logged in into identity provider will not be able to access any of the pages. Additionaly, when SAML is enabled, Building Bridges will use USER ID passed by identity provider to distinguish users (which should be 100% accurate, since only cookie and IP verification may fail). However, using SSO makes Building Bridges not fully anonymous.

You can read more about SAML [here](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language).

To enable SAML authorization in Building Bridges, you need to pass `SAML_ENABLED` flag to program, and set proper environment variables (please see **Configuration** table in README file)

---

Metadata for **building bridges** for IdP:

```
<?xml version="1.0" encoding="UTF-8"?>
    <md:EntityDescriptor entityID="<DOMAIN_OF_BRIDGES_WEBSITE>"
    xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata">
    <md:SPSSODescriptor AuthnRequestsSigned="false" WantAssertionsSigned="true" protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    md:NameIDFormaturn:oasis:names:tc:SAML:2.0:nameid-format:transient</md:NameIDFormat>
    md:NameIDFormaturn:oasis:names:tc:SAML:2.0:nameid-format:persistent</md:NameIDFormat>
    md:NameIDFormaturn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress</md:NameIDFormat>
    md:NameIDFormaturn:oasis:names:tc:SAML:1.1:nameid-format:unspecified</md:NameIDFormat>
    <md:AssertionConsumerService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="<DOMAIN_OF_BRIDGES_WEBSITE>/oauth2/callback/saml" index="0"/>
    </md:SPSSODescriptor>
</md:EntityDescriptor>
```

(change `<DOMAIN_OF_BRIDGES_WEBSITE>` to your domain)

---

## Developing and testing SAML

It's hard to develop, maintain and test parts of code with SAML authentication, since most often Identity Provider is hosted on the Internet, we develop things locally so IdP has no access to localhost. That's why to test it properly, we recommend hosting an IdP mock on localhost - great and easy to use example is [saml-idp](https://www.npmjs.com/package/saml-idp), written in *nodejs*.

After creating a keypair with command:
```
openssl req -x509 -new -newkey rsa:2048 -nodes -subj '/C=US/ST=California/L=San Francisco/O=JankyCo/CN=Test Identity Provider' -keyout idp-private-key.pem -out idp-public-cert.pem -days 7300
````

Sample IdP using this library with Building Bridges can be:

```
const {runServer} = require('saml-idp');
 
runServer({
  acsUrl: `http://localhost:8888/oauth2/callback/saml/`,
  audience: `http://localhost:8888`,
});
```

Then you can start your local IdP with `nodejs app_name.js`. After that, you need to set proper configuration fields related to SAML (please see **Configuration** table in README file)

