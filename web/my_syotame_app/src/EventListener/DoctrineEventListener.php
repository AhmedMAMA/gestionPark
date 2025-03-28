<?php
// src/EventListener/DoctrineEventListener.php

namespace App\EventListener;
use Doctrine\ORM\Event\PrePersistEventArgs;
use Doctrine\ORM\Event\LifecycleEventArgs;
use App\Entity\User;

class DoctrineEventListener
{
    // Méthode appelée avant de persister l'entité
    public function prePersist(PrePersistEventArgs $args)
    {
        // Récupérer l'entité à partir de l'argument
        $monEntite = $args->getObject();  // Utilise `getObject()` pour récupérer l'entité

        // Vérifie si l'entité est de type User
        if ($monEntite instanceof User) {
            // Définir createdAt si ce n'est pas déjà fait
            if ($monEntite->getCreatedAt() === null) {
                $monEntite->setCreatedAt(new \DateTimeImmutable());
            }
            // Toujours définir updatedAt lors de la création
            $monEntite->setUpdatedAt(new \DateTimeImmutable());
        }
    }

    // Méthode appelée avant de mettre à jour l'entité
    public function preUpdate(LifecycleEventArgs $args)
    {
        // Récupérer l'entité à partir de l'argument
        $monEntite = $args->getEntity();

        // Vérifie si l'entité est de type User
        if ($monEntite instanceof User) {
            // Mettre à jour updatedAt lors de la mise à jour
            $monEntite->setUpdatedAt(new \DateTimeImmutable());
        }
    }
}
