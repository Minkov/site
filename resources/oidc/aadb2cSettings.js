var tenantName = "telerikacademyauth.onmicrosoft.com";
var signInSignUpPolicyName = "B2C_1A_signup_signin";
var passwordResetPolicyName = "B2C_1A_PasswordReset";
var loginBaseUrl = "https://login.microsoftonline.com/";
var base_uri = "https://192.168.160.22:8043/";
var redirectUri = base_uri + "signin-oidc";

var applicationId = 'f2b7f557-f20a-4655-a222-05fc3d73be36';

var helloNetwork = {
    adB2CSignInSignUp: 'adB2CSignInSignUp',
    adB2CPasswordReset: 'adB2CPasswordReset'
};

hello.init({
    adB2CSignInSignUp: {
        oauth: {
            version: 2,
            auth: loginBaseUrl + "tfp/" + tenantName + "/" + signInSignUpPolicyName + "/oauth2/v2.0/authorize",
            grant: loginBaseUrl + "tfp/" + tenantName + "/" + signInSignUpPolicyName + "/oauth2/v2.0/token"
        },
        scope_delim: ' ',
        logout: function () {
            var id_token = hello(helloNetwork.adB2CSignInSignUp).getAuthResponse().id_token;
            hello.utils.store(helloNetwork.adB2CSignInSignUp, null);
            window.location = loginBaseUrl + tenantName + "/oauth2/v2.0/logout?p=" + signInSignUpPolicyName + "&id_token_hint=" +
                id_token + "&post_logout_redirect_uri=" + base_uri;
        },
        form: false
    },
    adB2CPasswordReset: {
        oauth: {
            version: 2,
            auth: loginBaseUrl + "tfp/" + tenantName + "/" + passwordResetPolicyName + "/oauth2/v2.0/authorize",
            grant: loginBaseUrl + "tfp/" + tenantName + "/" + passwordResetPolicyName + "/oauth2/v2.0/token"
        },
        scope_delim: ' ',
        logout: function () {
            var id_token = hello(helloNetwork.adB2CPasswordReset).getAuthResponse().id_token;
            hello.utils.store(helloNetwork.adB2CPasswordReset, null);
            window.location = loginBaseUrl + tenantName + "/oauth2/v2.0/logout?p=" + passwordResetPolicyName + "&id_token_hint=" +
                id_token + "&post_logout_redirect_uri=" + base_uri;
        },
        form: false
    }
}, {
        redirect_uri: redirectUri,
        scope: 'openid ' + applicationId,
        response_type: 'token id_token',
        page_uri: redirectUri
    });

hello.init({
    adB2CSignInSignUp: applicationId,
    adB2CPasswordReset: applicationId
});