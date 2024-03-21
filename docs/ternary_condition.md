# Ternary condition

We have different way to compress ternary conditions

## ( variable == null) ? null : variable.()

```js
r = r == null ? null : r.CW;
```

becomes

```js
r == r?.CW;
```

## ( variable == null) ? null : variable.()

```js
r = r == null ? null : r.CW;
```

becomes

```js
r == r?.CW;
```

## Use min or max

Some ternary conditions are just `min()` and `max()` functions. It's not shorter if we use the `Math.min` function but with an alias like `var min = Math.min`

```js
c < d ? c : d;
```

becomes

```js
Math.min(c, d);
```
