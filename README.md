# CTFd Route Manager

A CTFd plugin to manage HTTP redirects directly from the admin panel — no code editing required.

## Features

- Add 301 (permanent) or 302 (temporary) redirects between relative paths
- Enable or disable each redirect individually without deleting it
- Delete redirects at any time
- Admin and plugin routes are always protected from being redirected

<img width="1332" height="868" alt="route" src="https://github.com/user-attachments/assets/36b57c07-5b1f-4017-bdd2-7dc2c2f51708" />


## Installation

Copy the `ctfd-route-manager` folder into your CTFd `plugins/` directory:

```
CTFd/plugins/ctfd-route-manager/
```

Restart CTFd. A **Route Manager** entry will appear in the admin plugin menu.

## Usage

1. Go to **Admin > Plugins > Route Manager**
2. Fill in a **source path** (e.g. `/old-page`) and a **destination path** (e.g. `/new-page`)
3. Choose the HTTP code: `302` (temporary) or `301` (permanent)
4. Click **Add** — the redirect is active immediately

From the table you can toggle (enable/disable) or delete any redirect.

> Both source and destination must be relative paths starting with `/`. External URLs are not allowed.

## Dependencies

- CTFd >= v3.x
- Compatible with Docker and local installations
- An up-to-date browser with JavaScript enabled
- CTFd theme: Core-beta

## Support

For any question or issue, open an [issue](https://github.com/votre-utilisateur/ctfd-route-manager/issues).
Or contact us on the Hack'olyte association website: [contact](https://hackolyte.fr/contact/).

## Contributing

Contributions are welcome!
You can:

- Report bugs
- Suggest new features
- Submit pull requests

## License

This plugin is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).
