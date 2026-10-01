from datetime import timedelta
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import Skill, User
from posts.models import Comment, Like, Post


class Command(BaseCommand):
    help = "Crea usuarios, perfiles, publicaciones e interacciones de demostracion."

    def handle(self, *args, **options):
        skill_names = [
            "Django",
            "Python",
            "HTML",
            "Tailwind CSS",
            "SQLite",
            "Diseno UX",
            "Fotografia",
            "Cocina",
            "Ceramica",
            "Deportes",
            "Literatura",
        ]
        skills = {name: Skill.objects.get_or_create(name=name)[0] for name in skill_names}

        demo_users = [
            ("admin_demo", "admin@aulagram.test", User.Role.ADMIN),
            ("creador_demo", "creador@aulagram.test", User.Role.CREATOR),
            ("estudiante_demo", "estudiante@aulagram.test", User.Role.MEMBER),
        ]
        for username, email, role in demo_users:
            user, created = User.objects.get_or_create(
                username=username, defaults={"email": email, "role": role}
            )
            if created:
                user.set_password("AulaGram2026!")
                user.save()
                user.profile.bio = "Cuenta creada para explorar el proyecto educativo."
                user.profile.save()
                user.profile.skills.set(
                    [skills["Django"], skills["Python"], skills["HTML"]]
                )
                self.stdout.write(self.style.SUCCESS(f"Creado: {username}"))
            else:
                self.stdout.write(f"Ya existe: {username}")

        people = [
            {
                "username": "sofia.ramos",
                "email": "sofia.ramos@aulagram.test",
                "first_name": "Sofia",
                "last_name": "Ramos",
                "role": User.Role.CREATOR,
                "bio": "Estudiante de UX. Convierto ideas y cafe en interfaces bonitas.",
                "location": "Ciudad de Panama",
                "website": "https://example.com/sofia",
                "avatar": "sofia.png",
                "skills": ["Diseno UX", "HTML", "Tailwind CSS"],
            },
            {
                "username": "mateo.codes",
                "email": "mateo.codes@aulagram.test",
                "first_name": "Mateo",
                "last_name": "Castillo",
                "role": User.Role.CREATOR,
                "bio": "Aprendiendo Django un commit a la vez. Cafe, codigo y plantas.",
                "location": "San Miguelito",
                "website": "https://example.com/mateo",
                "avatar": "mateo.png",
                "skills": ["Django", "Python", "SQLite"],
            },
            {
                "username": "vale.camina",
                "email": "vale.camina@aulagram.test",
                "first_name": "Valeria",
                "last_name": "Brown",
                "role": User.Role.CREATOR,
                "bio": "Rincones de Panama, caminatas y fotos con mucha luz.",
                "location": "Panama",
                "website": "",
                "avatar": "vale.png",
                "skills": ["Fotografia"],
            },
            {
                "username": "nico.horno",
                "email": "nico.horno@aulagram.test",
                "first_name": "Nicolas",
                "last_name": "Mendez",
                "role": User.Role.MEMBER,
                "bio": "Pan casero, recetas simples y el desorden honesto de mi cocina.",
                "location": "Betania",
                "website": "",
                "avatar": "nico.png",
                "skills": ["Cocina"],
            },
            {
                "username": "luna.ceramica",
                "email": "luna.ceramica@aulagram.test",
                "first_name": "Luna",
                "last_name": "Herrera",
                "role": User.Role.CREATOR,
                "bio": "Ceramica lenta, manos sucias y piezas con personalidad.",
                "location": "El Cangrejo",
                "website": "https://example.com/luna",
                "avatar": "luna.png",
                "skills": ["Ceramica", "Fotografia"],
            },
            {
                "username": "dani.hoops",
                "email": "dani.hoops@aulagram.test",
                "first_name": "Daniel",
                "last_name": "Joseph",
                "role": User.Role.MEMBER,
                "bio": "Estudiante, base del equipo y defensor de los partidos al atardecer.",
                "location": "Parque Lefevre",
                "website": "",
                "avatar": "dani.png",
                "skills": ["Deportes"],
            },
            {
                "username": "ines.lee",
                "email": "ines.lee@aulagram.test",
                "first_name": "Ines",
                "last_name": "Navarro",
                "role": User.Role.MEMBER,
                "bio": "Literatura, lluvia y Miso, el verdadero dueno de mi apartamento.",
                "location": "Bella Vista",
                "website": "",
                "avatar": "ines.png",
                "skills": ["Literatura"],
            },
        ]

        social_users = {}
        avatar_dir = Path(settings.BASE_DIR) / "seed_assets" / "avatars"
        for person in people:
            defaults = {
                "email": person["email"],
                "first_name": person["first_name"],
                "last_name": person["last_name"],
                "role": person["role"],
            }
            user, created = User.objects.get_or_create(
                username=person["username"], defaults=defaults
            )
            if created:
                user.set_password("AulaGram2026!")
                user.save()
            else:
                for field, value in defaults.items():
                    setattr(user, field, value)
                user.save()

            profile = user.profile
            profile.bio = person["bio"]
            profile.location = person["location"]
            profile.website = person["website"]
            if not profile.avatar:
                avatar_path = avatar_dir / person["avatar"]
                with avatar_path.open("rb") as avatar_file:
                    profile.avatar.save(person["avatar"], File(avatar_file), save=False)
            profile.save()
            profile.skills.set([skills[name] for name in person["skills"]])
            social_users[user.username] = user

        post_data = [
            (
                "mateo.codes",
                "workspace.png",
                "Nueva semana, nuevo proyecto. Hoy por fin entendi como se conectan URLs, vistas y templates en Django. ☕💻 #Django #Aprendiendo",
                2,
            ),
            (
                "vale.camina",
                "casco-viejo.png",
                "Una vuelta sin prisa por Casco. Siempre aparece un balcon nuevo que no habia visto. 🌺🚲",
                8,
            ),
            (
                "nico.horno",
                "cinnamon-rolls.png",
                "Primer intento de rollos de canela. No quedaron iguales, pero desaparecieron en diez minutos. Eso cuenta como exito, ¿no?",
                19,
            ),
            (
                "vale.camina",
                "waterfall.png",
                "La lluvia casi nos hace regresar, pero el sendero estaba increible. Panama verde de verdad. 🌿",
                31,
            ),
            (
                "luna.ceramica",
                "pottery.png",
                "Aprendiendo a dejar que la arcilla decida un poco. Esta taza termino siendo cuenco y me encanta.",
                45,
            ),
            (
                "dani.hoops",
                "basketball.png",
                "Partido improvisado despues de clases. Perdimos la cuenta, ganamos la tarde. 🏀",
                58,
            ),
            (
                "ines.lee",
                "cat-reading.png",
                "Miso dice que hoy no se estudia. Su argumento es bastante convincente. 📚🐈",
                76,
            ),
        ]

        asset_dir = Path(settings.BASE_DIR) / "seed_assets" / "posts"
        seeded_posts = []
        for username, filename, caption, hours_ago in post_data:
            author = social_users[username]
            post = Post.objects.filter(author=author, caption=caption).first()
            if post is None:
                post = Post(author=author, caption=caption)
                with (asset_dir / filename).open("rb") as image_file:
                    post.image.save(filename, File(image_file), save=False)
                post.save()
                Post.objects.filter(pk=post.pk).update(
                    created_at=timezone.now() - timedelta(hours=hours_ago)
                )
                post.refresh_from_db()
            seeded_posts.append(post)

        usernames = list(social_users)
        for post_index, post in enumerate(seeded_posts):
            # Patron estable: cada post recibe entre 3 y 5 likes diferentes.
            for offset in range(1, 5 + (post_index % 2)):
                liker = social_users[usernames[(post_index + offset) % len(usernames)]]
                if liker != post.author:
                    Like.objects.get_or_create(user=liker, post=post)

        comments = [
            (0, "sofia.ramos", "¡Ese escritorio pide una sesion de estudio!"),
            (0, "ines.lee", "La planta al lado del monitor es clave 🌱"),
            (1, "mateo.codes", "Que luz tan bonita. Parece de pelicula."),
            (1, "luna.ceramica", "Ese balcon lleno de flores 😍"),
            (2, "sofia.ramos", "Necesito la receta, se ven buenisimos."),
            (2, "dani.hoops", "Confirmo que no habrian durado ni cinco minutos conmigo."),
            (3, "nico.horno", "Anotado para el proximo fin de semana."),
            (3, "ines.lee", "Se siente la lluvia solo con mirar la foto."),
            (4, "vale.camina", "Las piezas imperfectas siempre son las mejores."),
            (4, "sofia.ramos", "Ese color natural quedo precioso."),
            (5, "mateo.codes", "La revancha la proxima semana 🏀"),
            (5, "nico.horno", "Yo llevo algo para despues del partido."),
            (6, "luna.ceramica", "Miso tiene toda la razon."),
            (6, "vale.camina", "Plan perfecto para una tarde de lluvia."),
        ]
        for post_index, username, body in comments:
            Comment.objects.get_or_create(
                post=seeded_posts[post_index], user=social_users[username], body=body
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Feed listo: {len(social_users)} perfiles, "
                f"{len(seeded_posts)} publicaciones, "
                f"{Like.objects.filter(post__in=seeded_posts).count()} likes y "
                f"{Comment.objects.filter(post__in=seeded_posts).count()} comentarios."
            )
        )
        self.stdout.write(self.style.WARNING("Contrasena demo: AulaGram2026!"))
