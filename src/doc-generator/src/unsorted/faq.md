# Frequently Asked Questions

:::warning Work in progress
<centered-image src="/img/work-in-progress.png" />
This warning will be removed once this page has passed testing.
:::

<faq-entry>
  <template #question>
    I need to connect my service to other service providers.  What is the best practice?
  </template>
  <template #answer>
    Integration.  Use <code>hy integration create...</code> etc...
  </template>
</faq-entry>


<faq-entry>
  <template #question>
    I need to serve and reference static content (images, videos, etc.).  How do I do this?     
  </template>
  <template #answer>
    <code>HY_MEDIA_BASE_URL</code>, <code>hy integration create s3</code>, more...        
  </template>
</faq-entry>

<faq-entry>
  <template #question>
    What's up with settings fields having both Optional and default=None?
  </template>
  <template #answer>
    Optional allows the value to be None.  default=None allows the environment variable to not be specified.  (elaborate)
  </template>
</faq-entry>
