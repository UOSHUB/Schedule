// Store a reference of window location
var page = window.location;
// Split host name into it's parts
var hostParts = page.host.split('.');
// If the used protocol is "https"
if(page.protocol == "https:") {
    // If it's any url other than heroku's
    if(hostParts[1] != "herokuapp") {
        // Redirect to "http" instead
        page.replace(page.href.replace("https", "http"));
    }
// Otherwise, if subdomain isn't "www"
} else if(hostParts[0] != "www") {
    // If a subdomain isn't specified in url
    if(hostParts.length == 2) {
        // Redirect to "www" as it's the default subdomain
        page.replace(page.href.replace("//", "//www."));
    // If it's heroku's default "http" url
    } else if(hostParts[1] == "herokuapp") {
        // Redirect to "https" instead
        page.replace(page.href.replace("http", "https"));
    // If the subdomain is "source" or "github"
    } else if(hostParts[0] == "source" || hostParts[0] == "github") {
        // Redirect to UOSHUB repo source on github
        page.replace("https://github.com/OmarEinea/UOSHUB");
    }
}
