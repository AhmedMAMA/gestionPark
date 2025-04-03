use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use std::fs;

fn main() -> PyResult<()> {
    // Définir le chemin vers le fichier main.py
    let chemin_script = "/home/ahmed/Desktop/Projet/OpenCV/main.py";

    // Lire le contenu du fichier main.py
    let code_python = fs::read_to_string(chemin_script)
        .expect("Impossible de lire le fichier main.py");

    // Exécuter le script Python en s'assurant d'avoir le GIL
    Python::with_gil(|py| {
        // Modifier sys.path pour inclure le répertoire contenant le module "classes"
        let sys = py.import("sys")?;
        let path: &PyList = sys.getattr("path")?.downcast()?;
        path.insert(0, "/home/ahmed/Desktop/Projet/OpenCV")?;

        // Créer un dictionnaire global "bound" et définir __file__
        let globals = PyDict::new_bound(py);
        globals.set_item("__file__", chemin_script)?;

        // Exécuter le script avec le dictionnaire des globals bound
        py.run_bound(&code_python, Some(&globals), None)
            .expect("Erreur lors de l'exécution du script Python");
        Ok(())
    })
}
