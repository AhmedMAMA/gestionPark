<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use App\Repository\ParkingRepository;

final class ViewControllersController extends AbstractController
{
    #[Route('/', name: 'app_view_controllers')]
    public function index(ParkingRepository $parking): Response
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $freeplace = $parking->AllFreePlace();
        return $this->render('view_controllers/index.html.twig', [
            'freeplace' => $freeplace,
        ]);
    }
}
