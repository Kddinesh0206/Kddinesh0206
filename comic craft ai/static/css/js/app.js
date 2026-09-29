document.addEventListener(
    "DOMContentLoaded",
    () => {

        const form =
            document.querySelector(
                "#comic-form"
            );

        const button =
            document.querySelector(
                "#generate-btn"
            );


        if (!form || !button) {
            return;
        }


        form.addEventListener(
            "submit",
            () => {

                button.disabled = true;

                button.innerHTML =
                    "⏳ Creating your comic... please wait";

            }
        );

    }
);