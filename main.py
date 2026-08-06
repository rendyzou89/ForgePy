from core.project_generator import ProjectGenerator


def main() -> None:

    print("=" * 40)
    print(" ForgePy ")
    print("=" * 40)

    project_name = input("Project Name : ").strip()
    location = input("Location : ").strip()

    generator = ProjectGenerator()

    generator.create(
        project_name=project_name,
        location=location,
        template_name="basic",
    )


if __name__ == "__main__":
    main()