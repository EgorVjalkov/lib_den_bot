import tortoise
import connection_config as con


class Task(tortoise.models.Model):
    id = tortoise.fields.IntField(primary_key=True)
    name = tortoise.fields.CharField(max_length=254)
    description = tortoise.fields.CharField(max_length=498)
    date_created = tortoise.fields.DatetimeField(auto_now_add=True)
    date_updated = tortoise.fields.DatetimeField(auto_now=True)

    class Meta:
        table = "tasks"


async def main():
    await tortoise.Tortoise.init(
        db_url=f'postgres://{con.user}:{con.password}@{con.host}:5432/probe',
        modules={'models': ['__main__']}, # путь для моделек
    )
    await tortoise.Tortoise.generate_schemas()

    task = await Task.create(
        name="First task",
        description="First task description"
    )
    # Output: <Task>
    print(task.name)
    # Output: First task

    task.name = "First task updated name"
    await task.save()
    print(task.name)
    # Output: First task updated name

    await tortoise.Tortoise.close_connections()

if __name__ == "__main__":
    tortoise.run_async(main())
