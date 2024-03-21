# Array reduction

## Concecutive repeating elements

Crawl an array and replace the consecutive repeating elements with `...Array(length).fill(value)`
/!\ Compute that the length of the `...Array().fill()` is shorter than the current array

```js
[1, 1, 1, 1, 1, 1, 1, 1, 2, 2],
```

becomes

```js
[...Array(8).fill(1), 2, 2];
```

#

```js
[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99, 100];
```

becomes

```js
[...Array(10).map((x) => x * 10), 95, 99, 100];
```
