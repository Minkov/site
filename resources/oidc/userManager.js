var config = {
    authority: "https://auth.telerikacademy.com",
    client_id: "judge_test",
    response_type: "id_token token",
    scope: "openid profile email",
    redirect_uri: "http://192.168.160.24:8081/signin_oidc.html",
    post_logout_redirect_uri: "http://192.168.160.24:8081/logout",
};

var userManager = new UserManager(config);