# Fonts

# Duplication of function calls

```js
B.Gj=new A.i(!0,B.u,null,"Segoe UI",null,null,null,null,null,null,null,null,null,null,null,null,null,B.e,null,null,null,"blackRedmond displayLarge",null,null,null,null)
B.Fw=new A.i(!0,B.u,null,"Segoe UI",null,null,null,null,null,null,null,null,null,null,null,null,null,B.e,null,null,null,"blackRedmond displayMedium",null,null,null,null)
B.HC=new A.i(!0,B.u,null,"Segoe UI",null,null,null,null,null,null,null,null,null,null,null,null,null,B.e,null,null,null,"blackRedmond displaySmall",null,null,null,null)
B.EN=new A.i(!0,B.u,null,"Segoe UI",null,null,null,null,null,null,null,null,null,null,null,null,null,B.e,null,null,null,"blackRedmond headlineLarge",null,null,null,null)
B.Hk=new A.i(!0,B.u,null,"Segoe UI",null,null,null,null,null,null,null,null,null,null,null,null,null,B.e,null,null,null,"blackRedmond headlineMedium",null,null,null,null)
B.Er=new A.i(!0,B.w,null,"Segoe UI",null,null,null,null,null,null,null,null,null,null,null,null,null,B.e,null,null,null,"blackRedmond headlineSmall",null,null,null,null)
B.FW=new A.i(!0,B.w,null,"Segoe UI",null,null,null,null,null,null,null,null,null,null,null,null,null,B.e,null,null,null,"blackRedmond titleLarge",null,null,null,null)
B.G9=new A.i(!0,B.w,null,"Segoe UI",null,null,null,null,null,null,null,null,null,null,null,null,null,B.e,null,null,null,"blackRedmond titleMedium",null,null,null,null)
B.Eh=new A.i(!0,B.l,null,"Segoe UI",null,null,null,null,null,null,null,null,null,null,null,null,null,B.e,null,null,null,"blackRedmond titleSmall",null,null,null,null)
B.H0=new A.i(!0,B.w,null,"Segoe UI",null,null,null,null,null,null,null,null,null,null,null,null,null,B.e,null,null,null,"blackRedmond bodyLarge",null,null,null,null)
B.EP=new A.i(!0,B.w,null,"Segoe UI",null,null,null,null,null,null,null,null,null,null,null,null,null,B.e,null,null,null,"blackRedmond bodyMedium",null,null,null,null)
B.HR=new A.i(!0,B.u,null,"Segoe UI",null,null,null,null,null,null,null,null,null,null,null,null,null,B.e,null,null,null,"blackRedmond bodySmall",null,null,null,null)
B.Ga=new A.i(!0,B.w,null,"Segoe UI",null,null,null,null,null,null,null,null,null,null,null,null,null,B.e,null,null,null,"blackRedmond labelLarge",null,null,null,null)
B.EF=new A.i(!0,B.l,null,"Segoe UI",null,null,null,null,null,null,null,null,null,null,null,null,null,B.e,null,null,null,"blackRedmond labelMedium",null,null,null,null)
B.EW=new A.i(!0,B.l,null,"Segoe UI",null,null,null,null,null,null,null,null,null,null,null,null,null,B.e,null,null,null,"blackRedmond labelSmall",null,null,null,null)
```

We got this kind of block of functions several times. It would be nice if we could make another function like this :

```js
var x = (a,b) => new A.i(!0,a,null,"Segoe UI",null,null,null,null,null,null,null,null,null,null,null,null,null,B.e,null,null,null,b,null,null,null,null)
B.Gj=x(B.u,"blackRedmond displayLarge")
B.Fw=x(B.u,"blackRedmond displayMedium")
B.HC=x(B.u,"blackRedmond displaySmall")
B.EN=x(B.u,"blackRedmond headlineLarge")
B.Hk=x(B.u,"blackRedmond headlineMedium")
B.Er=x(B.w,"blackRedmond headlineSmall")
B.FW=x(B.w,"blackRedmond titleLarge")
B.G9=x(B.w,"blackRedmond titleMedium")
B.Eh=x(B.l,"blackRedmond titleSmall")
B.H0=x(B.w,"blackRedmond bodyLarge")
B.EP=x(B.w,"blackRedmond bodyMedium")
B.HR=x(B.u,"blackRedmond bodySmall")
B.Ga=x(B.w,"blackRedmond labelLarge")
B.EF=x(B.l,"blackRedmond labelMedium")
B.EW=x(B.l,"blackRedmond labelSmall")
```

We saves **1800** bytes. I can count 17 block of this type in a basic web build.