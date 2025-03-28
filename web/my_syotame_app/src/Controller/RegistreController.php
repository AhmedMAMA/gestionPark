<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use Symfony\Bundle\SecurityBundle\Security;
use App\Entity\User;
use App\Form\RegistrationType;
use Doctrine\ORM\EntityManagerInterface;
use App\Security\SecurityController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;

final class RegistreController extends AbstractController
{
    #[Route('/registre', name: 'app_registre')]
    public function index(Request $request, UserPasswordHasherInterface $userPasswordHasher, Security $security, EntityManagerInterface $entityManager): Response
    {
        $user = new User();
        $form = $this->createForm(RegistrationType::class, $user);
        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            /** @var string $password */
            $password = $form->get('password')->getData();
            // $handicap_ways = $form->get('handicap_way')->getData();

            // encode the plain password
            $user->setPassword($userPasswordHasher->hashPassword($user, $password));

            // dd($form->getData());

            $entityManager->persist($user);
            $entityManager->flush();

            // do anything else you need here, like send an email

            return $this->redirectToRoute('app_login'); // ou 'homepage' selon votre logique
            // return $security->login($user, SecurityController::class, 'main');
        }

        return $this->render('registre/index.html.twig', [
            'controller_name' => 'RegistreController',
            'registrationForm' => $form,
        ]);
    }
}
