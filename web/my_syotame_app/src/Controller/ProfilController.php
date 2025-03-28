<?php

namespace App\Controller;

use Doctrine\ORM\EntityManagerInterface;  // Importer l'interface correcte
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Bundle\SecurityBundle\Security;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

final class ProfilController extends AbstractController
{
    #[Route('/profil', name: 'app_profil')]
    public function index(Security $security): Response
    {
        // Récupérer l'utilisateur connecté
        $user = $security->getUser();

        if ($user) {
            // Si l'utilisateur est connecté, récupérer les informations
            $fullname = $user->getFullname();
            $isHandicapWay = $user->isHandicapWay();
            $email = $user->getEmail();
            $username = $user->getUserIdentifier();
        } else {
            // Si l'utilisateur n'est pas connecté, définir des valeurs par défaut
            $fullname = 'Utilisateur non connecté';
            $email = 'Email non disponible';
            $username = 'Utilisateur non connecté';
            $isHandicapWay = NULL;
        }

        return $this->render('profil/index.html.twig', [
            'controller_name' => 'ProfilController',
            'fullname' => $fullname,
            'email' => $email,
            'username' => $username,
            'HandicWay'=> $isHandicapWay
        ]);
    }

    #[Route('/remove_myself', name: 'app_remove_profil')]
    public function remove(Security $security, EntityManagerInterface $entityManager): Response
    {
        // Récupérer l'utilisateur connecté
        $user = $security->getUser();

        if ($user) {
            // Déconnecter l'utilisateur avant la suppression de ses données
            $security->setToken(null);  // Déconnexion

            // Supprimer les données de l'utilisateur
            $entityManager->remove($user);
            $entityManager->flush();

            // Ajouter un message flash de succès
            $this->addFlash('success', 'Votre compte a été supprimé avec succès.');

            // Rediriger vers la page d'accueil ou une autre page
            return $this->redirectToRoute('app_home');  // Remplacez 'app_home' par la route de votre choix
        }

        // Si l'utilisateur n'est pas connecté, rediriger ou afficher une erreur
        $this->addFlash('error', 'Aucun utilisateur connecté.');
        return $this->redirectToRoute('app_login');
    }
}
