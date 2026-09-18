import sys
from pathlib import Path
from pypdf import PdfReader


def extraire_textes_pdf(dossier):
    dossier = Path(dossier)

    if not dossier.exists():
        print(f"Erreur : le dossier n'existe pas : {dossier}")
        return

    if not dossier.is_dir():
        print(f"Erreur : ce chemin n'est pas un dossier : {dossier}")
        return

    fichiers_pdf = sorted(dossier.glob("*.pdf"))

    if not fichiers_pdf:
        print("Aucun fichier PDF trouvé dans le dossier.")
        return

    fichier_sortie = dossier / "extraction.txt"

    with open(fichier_sortie, "w", encoding="utf-8") as f:
        for pdf in fichiers_pdf:
            print(f"Extraction : {pdf.name}")

            try:
                reader = PdfReader(pdf)

                # Séparateur indiquant le début d'un nouveau PDF
                f.write("\n" + "=" * 80 + "\n")
                f.write(f"FICHIER : {pdf.name}\n")
                f.write("=" * 80 + "\n\n")

                for page_num, page in enumerate(reader.pages, start=1):
                    texte = page.extract_text()

                    if texte:
                        f.write(texte)
                        f.write("\n")

            except Exception as e:
                print(f"Erreur avec {pdf.name} : {e}")
                f.write(f"\n[ERREUR lors de l'extraction de {pdf.name}]\n")

    print(f"\nTerminé !")
    print(f"Fichier généré : {fichier_sortie}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python extract_pdf.py <chemin_du_dossier>")
        sys.exit(1)

    extraire_textes_pdf(sys.argv[1])
