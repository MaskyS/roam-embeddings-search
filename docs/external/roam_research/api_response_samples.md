# Roam API Response Samples

This document contains actual response samples from the Roam Research API, collected empirically to understand the data structure.

## Key Findings

### 1. Page vs Block Structure
- **Pages** have `:node/title` but no `:block/string`
- **Blocks** have `:block/string` but no `:node/title`
- **Daily Note Pages** have both `:node/title` and `:log/id` attribute
- All entities have `:block/uid`

### 2. Recursive Children Selector
To get nested children, you must use the recursive selector syntax:
```clojure
{:block/children ...}  ; Gets ALL nested children recursively
```

Without the `...`, you only get immediate children with specified attributes.

### 3. Daily Note Identification
Daily notes can be identified by:
- Presence of `:log/id` attribute
- UID format: "MM-DD-YYYY"
- Title format: "Month DDth, YYYY"

## Sample Responses

### 1. Page with Children (Recursive)
```json
{
  ":node/title": "Roam Portal",
  ":block/children": [
    {
      ":block/uid": "vfjxXDGMf",
      ":block/string": "is an intra-graph [[search engine]] and [[visualizer]] for [[Roam Research]] by [[Dharam Kapila]]",
      ":block/_children": [
        {
          ":node/title": "Roam Portal",
          ":block/children": [
            {
              ":block/uid": "vfjxXDGMf",
              ":block/order": 0,
              ":block/string": "is an intra-graph [[search engine]] and [[visualizer]] for [[Roam Research]] by [[Dharam Kapila]]"
            }
          ],
          ":block/uid": "NGLXTbkDE"
        }
      ]
    }
  ],
  ":block/uid": "NGLXTbkDE"
}
```

### 2. Daily Note Page
```json
{
  ":node/title": "March 15th, 2021",
  ":block/uid": "03-15-2021",
  ":log/id": 1615766400000
}
```
Note: The `:log/id` is a timestamp that uniquely identifies daily notes.

### 3. Block with References and Parent Context
```json
{
  ":block/uid": "LidMjhZr4",
  ":block/string": "This will only get easier and flexible over time. For instance, a recent update brought [[collapsible parentheticals]], where you can insert some text inline, and allow the user to expand it to get more details.",
  ":block/_children": [
    {
      ":block/children": [
        {
          ":block/uid": "FLrx_lbNu",
          ":block/order": 0,
          ":block/string": "In Roam, you can indent a block under another one to show it's related to it, or expands upon the details to the parent block."
        },
        {
          ":block/uid": "2HpyE0F-w",
          ":block/order": 1,
          ":block/string": "This enables you to decide the depth at which you want to explore each idea, and get a bird's-eye view of a page very quickly."
        }
      ],
      ":block/uid": "vH6WbGy3j",
      ":block/string": "**Identable & Expandable thought = Programmable Context**"
    }
  ]
}
```

### 4. Block References
- Block references appear in text as `((block-uid))`
- Page references appear as `[[Page Title]]`
- The `:block/refs` attribute contains referenced entities but may be empty if not explicitly requested in selector

## Query Examples

### Get All Daily Notes
```clojure
[:find ?uid
 :where
 [?e :block/uid ?uid]
 [?e :log/id ?log-id]]
```

### Get All Pages with Titles
```clojure
[:find ?uid ?title
 :where
 [?e :node/title ?title]
 [?e :block/uid ?uid]]
```

### Get Blocks with References
```clojure
[:find ?uid ?string
 :where
 [?e :block/uid ?uid]
 [?e :block/string ?string]
 [?e :block/refs ?ref]]
```

## Pull-Many Performance

Testing batch sizes with the Roam API showed:
- **1 block**: ~3.0s (3.0s per block)
- **10 blocks**: ~3.0s (0.3s per block)
- **50 blocks**: ~3.8s (0.076s per block)
- **100 blocks**: ~4.3s (0.043s per block)

Recommendation: Use batch sizes of 50-100 for optimal throughput.

## Important Selectors

### Full Context Selector (from sync_full.py)
```clojure
[:block/uid
 :block/string
 :node/title
 {:block/children [:block/uid :block/string :block/order]}
 {:block/_children [:block/uid :block/string :node/title
                     {:block/children [:block/uid :block/string :block/order]}]}]
```

This selector gets:
- Basic block/page info
- Immediate children with order
- Parent context via `:block/_children` (reverse lookup)
- Sibling context (parent's children)

### Recursive Children Selector
```clojure
[:block/uid
 :block/string
 :node/title
 {:block/children ...}]  ; The ... makes it recursive
```

This gets the entire tree structure below a block/page.

## Next Steps for Chunking

With this understanding of the data structure:
1. Pages are natural grouping boundaries
2. Daily notes may need special handling due to interleaved topics
3. The `:block/order` attribute preserves hierarchy
4. Parent-child relationships provide context for semantic chunking