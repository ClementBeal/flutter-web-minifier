# String

## Factorisation of the strings

Some strings are repeated in the final JS code. If we have the same string twice and the length of both is smaller than `var XXX=<string>;XXX;XXX...`, then we can replace

For instance, `pointerdown` is repeated more than twice. We can store it in another variable to save some bytes

## No name

Some substrings are also repeated. For instance, `flutter/` is found at least 46 times in a basic build.
We can do some composition of this type :

Before

```js
var a = "flutter/textinput";
var b = "flutter/keyboard";
var c = "flutter/menu";
var d = "flutter/platform";
```

After

```js
var x = "flutter/";
var a = x + "textinput";
var b = x + "keyboard";
var c = x + "menu";
var d = x + "platform";
```
