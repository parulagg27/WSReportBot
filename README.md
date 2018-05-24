# hello-flask-react

This quickstart consists of a basic hasura project with a simple react as well as a flask(python microframework) app running on it. Once this project is deployed on to a hasura cluster, you will have the react app running at https://ui.cluster-name.hasura-app.io and the flask app will run at https://api.cluster-name.hasura-app.io

This is the right place to start if you are planning to build or want to learn to build a app combination of back-end(by flask) and front-end(by react) with hasura.

## Sections

* [Files and Directories](#files-and-directories)
* [Introduction](#introduction)
* [Quickstart](#quickstart)
* [Data API](#data-apis)
* [Auth API](#auth-apis)
* [Filestore API](#filestore-apis)
* [Custom service](#custom-service)
* [Support](#support)

## Files and Directories

The project (a.k.a. project directory) has a particular directory structure and it has to be maintained strictly, else `hasura` cli would not work as expected. A representative project is shown below:

```
.
├── hasura.yaml
├── clusters.yaml
├── conf
│   ├── authorized-keys.yaml
│   ├── auth.yaml
│   ├── ci.yaml
│   ├── domains.yaml
│   ├── filestore.yaml
│   ├── gateway.yaml
│   ├── http-directives.conf
│   ├── notify.yaml
│   ├── postgres.yaml
│   ├── routes.yaml
│   └── session-store.yaml
├── migrations
│   ├── 1504788327_create_table_userprofile.down.yaml
│   ├── 1504788327_create_table_userprofile.down.sql
│   ├── 1504788327_create_table_userprofile.up.yaml
│   └── 1504788327_create_table_userprofile.up.sql
└── microservices 
    ├── api
    └── ui
```
## Introduction

This quickstart project comes with the following by default:
* A basic hasura project
* Two tables `article` and `author` with some dummy data
* A basic react app which runs at the `ui` subdomain which fetches a list of articles available
* A basic python-flask app which runs on the `api` subdomain.

## Quickstart

Follow this section to get this project working. Before you begin, ensure you have the latest version of hasura cli tool installed.


### Step 1: Getting the project

```sh
$ hasura quickstart hello-flask-react
$ cd hello-flask-react
```

The above command does the following:
* Creates a new folder in the current working directory called `hello-flask-react`
* Creates a new trial hasura cluster for you and sets that cluster as the default cluster for this project
* Initializes `hello-flask-react` as a git repository and adds the necessary git remotes.
* Adds your SSH public key to the cluster so that you can push to it.

### Step 2: Getting cluster information

Every hasura project is run on a Hasura cluster. To get details about the cluster this project is running on:

```sh
$ hasura cluster status
```

This will give you your cluster status like so

```sh
INFO Status:                                      
Cluster Name:       basket40
Cluster Alias:      hasura
Kube Context:       basket40
Platform Version:   v0.15.23
Cluster State:      Synced
```

Keep a note of your cluster name. Alternatively, you can also go to your [hasura dashboard](https://dashboard.hasura.io) and see the clusters you have.

### Step 3: Deploying on a hasura cluster

* Open the package.json file at `microservices/ui/app/`
* Find the key `scripts` and then replace `cluster-name` with the name of your cluster (in this case, `basket40`) in the `build` & `start` key.

To deploy your app:

```sh
$ git add .
$ git commit -m "Initial Commit"
$ git push hasura master
```

Once the above commands are executed successfully, head over to `https://ui.cluster-name.hasura-app.io` (in this case `https://ui.basket40.hasura-app.io`) to view your react app.

Alternatively, you can use `hasura microservice open ui` to open the browser and navigate to that link automatically.

## Api console

Every hasura cluster comes with an api console that gives your a GUI to test out the baas features of hasura. To open the api console

```sh
$ hasura api-console
```

## Data APIs

Hasura provides ready to use data apis to make powerful data queries on your tables. This means that you have ready-to-use JSON apis on any tables created. The url to be used to make these queries is always of the type: `https://data.cluster-name.hasura-app.io/v1/query` (in this case `https://data.basket40.hasura-app.io`)

As mentioned earlier, this quickstart app comes with two pre-created tables `author` and `article`.

**author**

column | type
--- | ---
id | integer NOT NULL *primary key*
name | text NOT NULL

**article**

column | type
--- | ---
id | serial NOT NULL *primary key*
title | text NOT NULL
content | text NOT NULL
rating | numeric NOT NULL
author_id | integer NOT NULL

Alternatively, you can also view the schema for these tables on the api console by heading over to the tab named `data` as shown in the screenshots below.

![Data1](https://raw.githubusercontent.com/hasura/hello-react/master/readme-assets/data-1.png "Data1")

![Data2](https://raw.githubusercontent.com/hasura/hello-react/master/readme-assets/data-2.png "Data2")

This means that you can now leverage the hasura data queries to perform CRUD operations on these tables.

The react app uses these data apis to show the respective data, to see it in action check out `https://ui.cluster-name.hasura-app.io/data` (replace cluster-name with your cluster name) and check out `app.js` at `microservices/ui/app/src/app.js` to see how the calls are being made. You can also check out all the apis provided by Hasura from the api console by heading over to the `API EXPLORER` tab.

For eg, to fetch a list of all articles from the article table, you have to send the following JSON request to the data api endpoint -> `https://data.cluster-name.hasura-app.io/v1/query` (replace `cluster-name` with your cluster name)

```json
{
    "type": "select",
    "args": {
        "table": "article",
        "columns": [
            "id",
            "title",
            "content",
            "rating",
            "author_id"
        ]
    }
}
```

To learn more about the data apis, head over to our [docs](https://docs.hasura.io/0.15/manual/data/index.html)

## Auth APIs

Every app almost always requires some form of authentication. This is useful to identify a user and provide some sort of personalised experience to the user. Hasura provides various types of authentication (username/password, mobile/otp, email/password, Google, Facebook etc).  

You can try out these in the `API EXPLORER` tab of the `api console`. To learn more, check out our [docs](https://docs.hasura.io/0.15/manual/getting-started/index.html)

The react app in this quickstart shows us an example of the username/password authentication. To see it in action navigate to `https://auth.cluster-name.hasura-app.io/ui`.

![Screenshot (155).png](https://filestore.hasura.io/v1/file/862a3a2a-6d10-4c72-9033-5607d315551f)

## Filestore APIs

Sometimes, you would want to upload some files to the cloud. This can range from a profile pic for your user or images for things listed on your app. You can securely add, remove, manage, update files such as pictures, videos, documents using Hasura filestore.

You can try out these in the `API EXPLORER` tab of the `api console`. To learn more, check out our [docs](https://docs.hasura.io/0.15/manual/api-console/index.html)

## Custom Service

There might be cases where you might want to perform some custom business logic on your apis. For example, sending an email/sms to a user on sign up or sending a push notification to the mobile device when some event happens. For this, you would want to create your own custom service which does these for you on the endpoints that you define.

This quickstart comes with one such custom service written in `python` using the `flask` framework. Check it out in action at `https://api.cluster-name.hasura-app.io` . Currently, it just returns a "Hasura Hello World" at that endpoint.

In case you want to use another language/framework for your custom service. Take a look at our [docs](https://docs.hasura.io/0.15/manual/custom-microservices/index.html) to see how you can add a new custom service.

## Support

If you happen to get stuck anywhere, please mail me at ravivaniya4911@gmail.com. Alternatively, if you find a bug, you can raise an issue [here](https://github.com/ravivaniya4911/hello-flask-react/issues).