# Functions

## Math.min/max chaining

Some of the code contains Math.min/max chaining :

```js
a2[0] = Math.min(Math.min(Math.min(a0[0], a0[1]), a0[2]), a0[3]) / a;
```

Should be

```js
a2[0] = Math.min(a0[0], a0[1], a0[2], a0[3]) / a;
```

## Square root

Replace `Math.sqrt(x)` with `x**.5`

## Power

Replace `Math.pow(a,b)` with `x**b`

## Aliasing

Some functions that are called a lot should use an alias. For instance, `Math.max` ; `Math.min` and all the `Math` functions should use an alias

## Function factorisation

Put some functions into a variable

```js
new Float64Array(x)
new Float32Array()
...
```

Could be

```js
var a = (x) => new Float64Array(x),
  b = (x) => new Float32Array();
```

## RGBA functions

The JS uses code to extract Red, Green, Blue and Alpha values from an integer

```o>>>16&255,o>>>8&255,o&255`

We can define 8 functions :

- red : extract the red value
- blue : extract the blue value
- green : extract the green value
- alpha : extract the alpha value
- redN : extract the red value and divides by 255
- blueN : extract the blue value and divides by 255
- greenN : extract the green value and divides by 255
- alphaN : extract the alpha value and divides by 255
