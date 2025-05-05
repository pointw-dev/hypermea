# <span class="code">resource</span>

:::warning Work in progress
<centered-image src="/img/work-in-progress.png" />
This warning will be removed once this page has passed testing.
:::

intro

## create

* adds *resource-name* to the domain

* default fields are name, description

* add fields by modifying domain/*resource-name*.py - as you would any hypermea resource

* NOTE: resources in Eve are collections, so hypermea names resources as plural by convention,

    * i.e. if you enter `hy resource create dog` it will create an endpoint named **/dogs**

    * hypermea relies on the [inflect](https://pypi.org/project/inflect/) library for pluralization, which is very accurate but can make mistakes

    * If you want to specify the singular and plural names of a resource use "singular,plural" e.g.

## check

* shows the singular and plural forms of the resource hypermea will infer

## list

details

## remove

details
