# FF-10 — Approbation par empreinte attendue, protocole préalable

23 novembre 2026. Expérience limitée à la composition TodoMVC existante.

Une empreinte SHA-256 de la référence HTML est fixée AVANT les tests, hors des fichiers de projet modifiables. Le contrôleur exige cette empreinte et refuse de rendre si la référence fournie ne correspond pas. Trois scénarios : (1) candidat autorisé et référence intacte, rendu réel ; (2) modification de caption2 avec référence intacte, refus ; (3) modification de caption2 et remplacement de la référence par la même version modifiée, refus sur empreinte. Les rendus utilisent la V2 isolée, sans modifier le projet source.

Limite de confiance : si l'agent peut changer aussi l'empreinte attendue ou la commande qui la fournit, le verrou reste contournable. L'expérience ne constitue pas une signature humaine ni un système de permissions.
