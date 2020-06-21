from webdriver_manager.chrome import ChromeDriverManager
import zipfile
from selenium import webdriver


def build_manifest():
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """
    return manifest_json

def build_js(proxy_dict):
    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
              },
              bypassList: ["localhost"]
            }
          };
    
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }
    
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (proxy_dict['host'], proxy_dict['port'], proxy_dict['user'], proxy_dict['passwd'])
    return background_js


def get_chromedriver(proxy_dict=None, use_proxy=False, user_agent=None):
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", build_manifest())
            zp.writestr("background.js", build_js(proxy_dict))
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        chrome_options=chrome_options)
    return driver
