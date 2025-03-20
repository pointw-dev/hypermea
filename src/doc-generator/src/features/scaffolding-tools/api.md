# api

:::warning Work in progress
<centered-image src="/img/work-in-progress.png" />
This warning will be removed once this page has passed testing.
:::

There are three commands that run against `api`

| Sub command           | Description                                         |
|-----------------------|-----------------------------------------------------|
| [`create`](#create)   | `<name>`, or `.` to use the current folder's name   |
| [`addin`](#addin)     | Add an addin to an already created API              |
| [`version`](#version) | View or set the version number of the API           |


## create

Creates the API service.  This command is best run in an empty folder.

The first choice you must make is the name of the service.  This is the only required parameter.

```bash
hy api create .         # the service name will be the name of the folder you are in
hy api create whizbang  # the service name will be "whizbang"
```

### Add-ins

After the name, you can select from several add-ins which enhance your service.  All are optional, and you can choose as many as you wish.  You can add them at create time, or any time later.

To see the add-ins available. they are listed as Options when you type:

```bash
hy api create --help
```

The add-ins are:

| Add in                                       | Description                                                 |
|----------------------------------------------| ----------------------------------------------------------- |
| `-g` [`--add-git`](#--add-git)               | Initialize a local git repository                           |
| `-d` [`--add-docker`](#--add-docker)         | Add Dockerfile and supporting files                         |
| `-a` [`--add-auth`](#--add-auth)             | add authorization class and supporting files                |
| `-v` [`--add-validation`](#--add-validation) | add custom validation class that you can extend             |
| `-w` [`--add-websocket`](#--add-websocket)   | add web socket and supporting files                         |
| `-s` [`--add-serverless`](#--add-serverless) | EXPERIMENTAL: add serverless framework and supporting files |

> NOTE: You will find more details on each add-in in the next section.

You can mix and match these add-ins

```bash
hy api create foobar --add-docker --add-git
hy api create foobar -dg  # exactly the same as above
```

If you want all add-ins, the easiest way is:

```bash
hy api create foobar -davwsg
```

::: tip Note
When you select --add-git, it will always be added last as it performs the initial commit for you.  This way all the add-ins that are installed first will be part of the commit.
:::

## addin

If you didn't select an add-in when you created the API, you can always select it later with the `addin` command.

In other words...

```bash
hy api create foobar --add-validation
````

...is the same as...

```bash
hy api create foobar
hy api addin --add-validation
```

...no matter how much time passes between those two statements.

All the add-ins were introduced in the section above.  This section provides more details:

### --add-git

details

### --add-docker

* Adds the following files:
  `Dockerfile``
  ``docker-compose.yml` (note: by default this file does not use a volume for mongodb, so killing the container also kills your data)
  `.docker-ignore``
  ``image-build``
  ``image-build.bat`

  ...

### --add-auth

* Adds a folder named ``auth`` with modules to add authorization to your API (docs to come)
    * NOTE: the only supported IdP is [Auth0](https://auth0.com/) at the moment, but it will be fairly easy to manually tweak to use any OAuth2 JWT issuer. (I have used a forked [Glewlwyd](https://github.com/babelouest/glewlwyd) with very minimal changes)

### --add-validation

* adds a folder named `validation` with a module that adds custom validator to `HypermeaService`.  Use this to extend custom validations.  It comes with two validations:

    * `unique_ignorecase` - works exactly like the built-in `unique` validator except case is ignored

    * `unique_to_parent` - set this to a string of a resource's parent (singular!).  Uniqueness will only be applied to sibling resources, i.e. the same name can be used if the resource has a different parent.

        * e.g.

          ```bash
          hy resource create region
          hy resource create store
          hy link create region store
          ```

          Now in `domain.store`, change the name field definition from this:

          ```python
          'name": {
            'type': 'string',
                  ...
            'unique': True
          }
          ```

          to this:

          ```python
          'name": {
            'type': 'string',
                  ...
            'unique_to_parent': 'region'
          }
          ```

### --add-websocket

* Define other events/listeners, emitters/senders in `websocket/__init__.py` - feel free to remove the default stuff you see there
* There is a test client at `{{BASE_API_URL}}/_ws` (which you can remove in `websocket/__init__.py` by removing the `/_ws/chat` route)
    * This is useful to see how to configure the Javascript socket.io client to connect to the web socket now running in the API
    * It is also useful to test messages - the chat app merely re-emits what it receives

### --add-serverless

:::warning Experimental
<centered-image src="/img/experimental.svg" width="64"/>
This feature is experimental, under development, and kinda finicky - use with caution.
:::

* Adds the following files:

  `serverless.py` - instantiates, but doesn't run, the HypermeaService app object.  This object is made available to the serverless framework and is referenced in the `.yml` files

  `serverless-aws.yml`

  `serverless-azure.yml`

  `serverless-google.yml`

  `logging_no-files.yml` - copy this over the original `logging.yml` to eliminate logging to the file system (which is not available with serverless)

* Also installs serverless globally with npm, does an npm init in the root api folder, and locally installs some serverless plugins (node modules).

## version

View or set the version number of the API