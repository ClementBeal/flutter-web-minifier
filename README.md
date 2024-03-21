# Flutter web minifier

The goal of this project is to compress the `main.dart.js` that is about `3MB` non-compressed.

The final Javascript code generated is not optimized. We can apply some transformations to reduce condiderably the final size of this file.

## How does it work

We use an ECMAScript parser to get the JS tree. Then:

1. We crawl the tree to gather information and we apply some transformations (constant folding...)
2. We flatten the tree into a string and we apply some transformations (rational representation of the float...)

A list of the possibe transformations are available in the `docs` folder.

# Performance

On a blanck Flutter project, I was able to save 2% of the total file size with only 5 transformations.  
In the docs, I have listed more transformations  that can have a bigger impact.

# How can you help

For now, some transformations are applied but I have some struggle to just print a correct minified ECMAScript tree. Because of that, the final size is bigger than the initial one.

I'd need help to fix this issue and also, to implement the other transformations