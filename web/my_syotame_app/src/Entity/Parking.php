<?php

namespace App\Entity;

use App\Repository\ParkingRepository;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: ParkingRepository::class)]
class Parking
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 100)]
    private ?string $agency = null;

    #[ORM\Column(length: 100)]
    private ?string $address = null;

    #[ORM\Column]
    private ?int $full_place = null;

    #[ORM\Column]
    private ?int $hand_place = null;

    #[ORM\Column]
    private ?int $Occupied = null;

    #[ORM\Column]
    private ?\DateTimeImmutable $created_at = null;

    #[ORM\Column]
    private ?\DateTimeImmutable $updated_at = null;

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getAgency(): ?string
    {
        return $this->agency;
    }

    public function setAgency(string $agency): static
    {
        $this->agency = $agency;

        return $this;
    }

    public function getAddress(): ?string
    {
        return $this->address;
    }

    public function setAddress(string $address): static
    {
        $this->address = $address;

        return $this;
    }

    public function getFullPlace(): ?int
    {
        return $this->full_place;
    }

    public function setFullPlace(int $full_place): static
    {
        $this->full_place = $full_place;

        return $this;
    }

    public function getHandPlace(): ?int
    {
        return $this->hand_place;
    }

    public function setHandPlace(int $hand_place): static
    {
        $this->hand_place = $hand_place;

        return $this;
    }

    public function getOccupied(): ?int
    {
        return $this->Occupied;
    }

    public function setOccupied(int $Occupied): static
    {
        $this->Occupied = $Occupied;

        return $this;
    }

    public function getCreatedAt(): ?\DateTimeImmutable
    {
        return $this->created_at;
    }

    public function setCreatedAt(\DateTimeImmutable $created_at): static
    {
        $this->created_at = $created_at;

        return $this;
    }

    public function getUpdatedAt(): ?\DateTimeImmutable
    {
        return $this->updated_at;
    }

    public function setUpdatedAt(\DateTimeImmutable $updated_at): static
    {
        $this->updated_at = $updated_at;

        return $this;
    }
}
