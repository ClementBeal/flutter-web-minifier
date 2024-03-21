# Nested condition

```js
if (b instanceof A.qz)
  if (J.c(b.a, r.a))
    if (J.c(b.b, r.b))
      if (J.c(b.d, r.d))
        if (J.c(b.f, r.f))
          if (J.c(b.r, r.r))
            if (J.c(b.w, r.w))
              if (J.c(b.x, r.x))
                if (J.c(b.y, r.y))
                  if (b.z == r.z) s = !0;
                  else s = !1;
                else s = !1;
              else s = !1;
            else s = !1;
          else s = !1;
        else s = !1;
      else s = !1;
    else s = !1;
  else s = !1;
else s = !1;
```

Those nested conditions are not necessary. We can see that the `else` cases are the same. We should use the property of the `&&` operator that short-circut the conditions at the first `false`

We should obtain that:

```js
if (
  b instanceof A.qs &&
  b.a == r.a &&
  J.c(b.b, r.b) &&
  J.c(b.c, r.c) &&
  J.c(b.d, r.d) &&
  J.c(b.e, r.e) &&
  J.c(b.r, r.r) &&
  J.c(b.f, r.f) &&
  J.c(b.w, r.w) &&
  J.c(b.x, r.x) &&
  J.c(b.y, r.y) &&
  J.c(b.z, r.z) &&
  J.c(b.Q, r.Q) &&
  J.c(b.as, r.as) &&
  J.c(b.at, r.at) &&
  J.c(b.ax, r.ax) &&
  J.c(b.ay, r.ay) &&
  J.c(b.ch, r.ch) &&
  J.c(b.id, r.id) &&
  b.k1 == r.k1
) {
  s = !0;
} else {
  s = !1;
}
```
