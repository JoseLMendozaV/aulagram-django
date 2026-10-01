/* Interacciones progresivas de AulaGram: funcionan sin recargar y conservan
   los formularios HTML como alternativa cuando JavaScript no esta disponible. */
(() => {
    "use strict";

    const toastContainer = document.querySelector("[data-toast-container]");

    function showToast(message, type = "success") {
        if (!toastContainer) return;
        const toast = document.createElement("div");
        toast.className = [
            "pointer-events-auto translate-y-3 rounded-2xl border px-4 py-3 text-sm font-semibold opacity-0 shadow-xl transition duration-300",
            type === "error"
                ? "border-red-200 bg-red-50 text-red-800"
                : "border-slate-800 bg-slate-950 text-white",
        ].join(" ");
        toast.textContent = message;
        toastContainer.appendChild(toast);
        requestAnimationFrame(() => toast.classList.remove("translate-y-3", "opacity-0"));
        window.setTimeout(() => {
            toast.classList.add("translate-y-3", "opacity-0");
            window.setTimeout(() => toast.remove(), 300);
        }, 2600);
    }

    async function submitAjax(form) {
        const response = await fetch(form.action, {
            method: form.method || "POST",
            body: new FormData(form),
            headers: { "X-Requested-With": "XMLHttpRequest" },
            credentials: "same-origin",
        });
        const contentType = response.headers.get("content-type") || "";
        if (!contentType.includes("application/json")) {
            throw new Error("Tu sesion pudo haber expirado. Recarga la pagina.");
        }
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "No se pudo completar la accion.");
        return data;
    }

    document.addEventListener("submit", async (event) => {
        const form = event.target;

        if (form.matches("[data-like-form]")) {
            event.preventDefault();
            const card = form.closest("[data-post-id]");
            const button = form.querySelector("[data-like-button]");
            const icon = form.querySelector("[data-like-icon]");
            button.disabled = true;
            try {
                const data = await submitAjax(form);
                card.querySelector("[data-like-count]").textContent = data.count;
                button.setAttribute("aria-pressed", String(data.liked));
                icon.classList.toggle("fill-fuchsia-600", data.liked);
                icon.classList.toggle("text-fuchsia-600", data.liked);
                icon.classList.toggle("fill-none", !data.liked);
                icon.classList.toggle("text-slate-700", !data.liked);
            } catch (error) {
                showToast(error.message, "error");
            } finally {
                button.disabled = false;
            }
            return;
        }

        if (form.matches("[data-comment-form]")) {
            event.preventDefault();
            const input = form.querySelector("[name='body']");
            const errorText = form.querySelector("[data-form-error]");
            const button = form.querySelector("[data-submit-button]");
            if (!input.value.trim()) {
                errorText.textContent = "Escribe un comentario antes de publicar.";
                errorText.classList.remove("hidden");
                return;
            }
            errorText.classList.add("hidden");
            button.disabled = true;
            try {
                const data = await submitAjax(form);
                const list = form.closest("[data-post-id]").querySelector("[data-comments-list]");
                list.querySelector("[data-empty-comments]")?.remove();
                list.insertAdjacentHTML("beforeend", data.html);
                const inserted = list.querySelector(`[data-comment-id='${data.comment_id}']`);
                inserted?.animate(
                    [{ opacity: 0, transform: "translateY(6px)" }, { opacity: 1, transform: "translateY(0)" }],
                    { duration: 240, easing: "ease-out" }
                );
                form.reset();
                input.focus();
            } catch (error) {
                errorText.textContent = error.message;
                errorText.classList.remove("hidden");
            } finally {
                button.disabled = false;
            }
            return;
        }

        if (form.matches("[data-comment-delete-form]")) {
            event.preventDefault();
            const row = form.closest("[data-comment-id]");
            const button = form.querySelector("button");
            button.disabled = true;
            try {
                await submitAjax(form);
                await row.animate(
                    [{ opacity: 1, height: `${row.offsetHeight}px` }, { opacity: 0, height: 0 }],
                    { duration: 200, easing: "ease-in" }
                ).finished;
                row.remove();
                showToast("Comentario eliminado.");
            } catch (error) {
                button.disabled = false;
                showToast(error.message, "error");
            }
        }
    });

    document.querySelectorAll("[data-post-editor]").forEach((editor) => {
        const input = editor.querySelector("[data-image-input]");
        const preview = editor.querySelector("[data-image-preview]");
        const empty = editor.querySelector("[data-image-empty]");
        const dropZone = editor.querySelector("[data-drop-zone]");
        const caption = editor.querySelector("[data-caption-input]");
        const counter = editor.querySelector("[data-caption-count]");
        let objectUrl;

        const previewFile = (file) => {
            if (!file || !file.type.startsWith("image/")) {
                showToast("Selecciona un archivo de imagen valido.", "error");
                return;
            }
            if (objectUrl) URL.revokeObjectURL(objectUrl);
            objectUrl = URL.createObjectURL(file);
            preview.src = objectUrl;
            preview.classList.remove("hidden");
            empty.classList.add("hidden");
        };

        input?.addEventListener("change", () => previewFile(input.files[0]));
        ["dragenter", "dragover"].forEach((name) => dropZone?.addEventListener(name, (event) => {
            event.preventDefault();
            dropZone.classList.add("ring-2", "ring-fuchsia-500");
        }));
        ["dragleave", "drop"].forEach((name) => dropZone?.addEventListener(name, (event) => {
            event.preventDefault();
            dropZone.classList.remove("ring-2", "ring-fuchsia-500");
        }));
        dropZone?.addEventListener("drop", (event) => {
            const file = event.dataTransfer.files[0];
            if (!file) return;
            const transfer = new DataTransfer();
            transfer.items.add(file);
            input.files = transfer.files;
            previewFile(file);
        });

        const updateCounter = () => {
            if (counter && caption) counter.textContent = caption.value.length;
        };
        caption?.addEventListener("input", updateCounter);
        updateCounter();

        editor.addEventListener("submit", () => {
            const submit = editor.querySelector("[data-editor-submit]");
            submit.disabled = true;
            submit.querySelector("span").textContent = "Guardando...";
        });
    });

    document.querySelectorAll("[data-profile-editor]").forEach((editor) => {
        const input = editor.querySelector("[data-avatar-input]");
        const preview = editor.querySelector("[data-avatar-preview]");
        const fallback = editor.querySelector("[data-avatar-fallback]");
        const bio = editor.querySelector("[data-bio-input]");
        const counter = editor.querySelector("[data-bio-count]");
        let objectUrl;

        input?.addEventListener("change", () => {
            const file = input.files[0];
            if (!file || !file.type.startsWith("image/")) return;
            if (objectUrl) URL.revokeObjectURL(objectUrl);
            objectUrl = URL.createObjectURL(file);
            preview.src = objectUrl;
            preview.classList.remove("hidden");
            fallback.classList.add("hidden");
            fallback.classList.remove("grid");
        });

        const updateBioCount = () => {
            if (bio && counter) counter.textContent = bio.value.length;
        };
        bio?.addEventListener("input", updateBioCount);
        updateBioCount();

        editor.addEventListener("submit", () => {
            const submit = editor.querySelector("[data-profile-submit]");
            submit.disabled = true;
            submit.textContent = "Guardando...";
        });
    });
})();
