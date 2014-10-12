Smyt_task
=========

Test task Smyt's company.

Installation
--------------
```sh
git clone https://github.com/bilabon/smyt_task.git
cd smyt_task
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt --allow-all-external
make test
make init_syncdb
make migrate_data
make run
```

Information
--------------
 - You can set structure of models here `/admin/core/setting/1/`. After saving you can see a updated file `model.yml` in directory apps's core. Then you can migrate it by command `make migrate_data`
 - You can modify, update and create Users and Rooms at `https://smyt-task.herokuapp.com`

##### Working with grammarish
```sh
auto: AutoField
bigint: BigIntegerField
bool: BooleanField
char: CharField
date: DateField
datetime: DateTimeField
decimal: DecimalField
email: EmailField
file: FileField
float: FloatField
image: ImageField
int: IntegerField
ip: IPAddressField
gip: GenericIPAddressField
nbool: NullBooleanField
pint: PositiveIntegerField
psint: PositiveSmallIntegerField
slug: SlugField
sint: SmallIntegerField
text: TextField
time: TimeField
url: URLField
fk: ForeignKey
m2m: ManyToManyField
timestamp: DateTimeField```

##### Syntax
```sh
<ModelName>:
    [doc: docstring]
    <fieldname>[-type-alias]:
        [type: type-alias],
        [args: arglist],
        kwarg: value

Example:
Room:
    department:
        type: char
        blank: false
        max_length: 200
    spots:
        type: int
        blank: false
```
