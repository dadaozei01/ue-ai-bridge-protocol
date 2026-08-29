# Projectile Generator Example

Pattern used for a Sequencer-friendly generator:

- Implement movement and spawn logic in project C++.
- Expose settings with `UPROPERTY(EditAnywhere, BlueprintReadWrite, Interp, Category=...)`.
- Expose commands with `UFUNCTION(BlueprintCallable, CallInEditor, Category=...)`.
- Create ordinary Blueprint child classes for artists and level designers.

Recommended controls:

- `SpawnActorClass`: any Actor Blueprint to spawn, such as cube, coin, or character.
- `TargetActors`: array of world targets.
- `TargetOffsets`: array of local offset targets.
- `TargetSelectionMode`: sequential or random.
- `SpawnInterval`
- `TotalSpawnCount`
- `TravelDuration`
- `ArcHeight`
- `StartGenerating`
- `StopGenerating`
- `SpawnBurst`

Reflection changes require compiling and restarting UE.
