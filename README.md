<p align="center">
  <img src="https://uploadkon.ir/uploads/9a4806_24Black-White-Minimalist-Business-Logo.jpg" alt="Logo">
</p>

<p align="center">
  <img src="http://quto.iran13.xyz:2095" alt="quto" width="1000">
</p>


With this program, you can capture more beautiful and better logs from your application.










## install CoolDebug

Clone the project

```bash
  git clone https://github.com/persamplex/CoolDebug.git
```

Go to the project directory

```bash
  cd CoolDebug
```

Use install option

```bash
  python CoolDebug.py --install
```

## Features

- Coustom full Log
- Log.html output
- Fast and usefull
- Profile you program (with {timer} option)
- Easy to Debug



## Usage/Examples
here we go! lets have some Cool Examples!!

### stage 1
just for try 
```python
from CoolDebug import CoolDebug

log = CoolDebug()
log.debug('this is error message')
log.info('this is error message')
log.warning('this is error message')
log.error('this is error message')
log.critical('this is error message')
```

**output**: 
![pic](https://uploadkon.ir/uploads/d8db06_24Capture.jpg)





### stage 2
add config option and write your **log_format**
```python
from CoolDebug import CoolDebug

log = CoolDebug()
log.config(log_format='{tag} [{timer}] [{message}]')
log.debug('this is error message')
log.info('this is error message')
log.warning('this is error message')
log.error('this is error message')
log.critical('this is error message')
```

**output**: 
![pic](https://uploadkon.ir/uploads/a35106_24Capture.jpg)


### stage 3
you know what.. i want store my log in my desk so...
i can use **html_log** option to make a log.html file!!
```python
from CoolDebug import CoolDebug

log = CoolDebug()
log.config(
            html_log=True,
            log_format='{tag} [{timer}] [{message}]',
           )
log.debug('this is error message')
log.info('this is error message')
log.warning('this is error message')
log.error('this is error message')
log.critical('this is error message')
```

**output**: 
![pic](https://uploadkon.ir/uploads/0fb406_24Capture.jpg)

**log.html**:
![pic](https://uploadkon.ir/uploads/4be906_24Capture.jpg)


### stage 4
OMG somthing happend! i need to just see CRITICAL logs! lets use **show_critical** option
```python
from CoolDebug import CoolDebug

log = CoolDebug()
log.config(
            html_log=True,
            log_format='{tag} [{timer}] [{message}]',
            show_critical=True,
            show_debug=False,
            show_error=False,
            show_info=False,
            show_warning=False,
           )
log.debug('this is error message')
log.info('this is error message')
log.warning('this is error message')
log.error('this is error message')
log.critical('this is error message')
```

**output**: 
![pic](https://uploadkon.ir/uploads/11e606_24Capture.jpg)



### stage 5
Hmm... I don't need to see any logs from CoolDebug on my terminal. Let's turn it off with the **print_log** option.
```python
from CoolDebug import CoolDebug

log = CoolDebug()
log.config(
            html_log=True,
            log_format='{tag} [{timer}] [{message}]',
            print_log=False
           )
log.debug('this is error message')
log.info('this is error message')
log.warning('this is error message')
log.error('this is error message')
log.critical('this is error message')
```

**output**: 
From what you thought, there's nothing to show here! 😄


### stage 6
Are you in New York? Ah, yeah, it's okay, don't panic.

To change the timezone, just use the **my_timezone** option. 
``(I just edited the log format for show all time options)``
```python
from CoolDebug import CoolDebug

log = CoolDebug()
log.config(
            html_log=True,
            log_format='{tag} [{timer}] [{day}/{month}/{year}] [{hour}:{min}:{sec}.{msec}ms]  [{message}]',
            my_timezone='America/New_York'
           )
log.debug('this is error message')
log.info('this is error message')
log.warning('this is error message')
log.error('this is error message')
log.critical('this is error message')
```
**output**: 
![pic](https://uploadkon.ir/uploads/760b06_24Capture.jpg)


### stage 7
Do you need more monitoring over your code?

**log_format** have some Cool Options like:
**{filename}** and **{function}** or **{line_number}** and as you know **{timer}**
```python
from CoolDebug import CoolDebug

log = CoolDebug()
log.config(
            html_log=True,
            log_format=' [{filename} > {function} > {line_number}] [{timer}] {tag} [{message}]',
            # my_timezone='America/New_York'
           )
log.debug('this is error message')
log.info('this is error message')
log.warning('this is error message')
log.error('this is error message')
log.critical('this is error message')
```
**output**: 
![pic](https://uploadkon.ir/uploads/d94d06_24Capture.jpg)


## Authors

- [@dridop](https://t.me/dridop)

