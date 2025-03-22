# Pagination

:::warning Work in progress
<centered-image src="/img/work-in-progress.png" />
This warning will be removed once this page has passed testing.
:::

You can request that resource collections be split into pages.  You do this by specifying one or two parameters:
* `max_results`
  * no matter how large the collection, your GET requests will never return more items from that collection than this number
  * this sets the number of items per page
  * if you do not specify `max_results` the service will use the value of `HY_PAGINATION_DEFAULT`
* `page`
  * given a collection split into pages of `max_results` each, `page` lets you request which page you want to GET
  * if you do not specify `page` the service will use the value of `1`

<centered-image src="/img/pagination.svg" />

* `HY_PAGINATION_DEFAULT` - the default value used if you do not specify a `max_results`
* `HY_PAGINATION_LIMIT`   - if `max_results` is greater than this number, it is treated as if it was this number instead



