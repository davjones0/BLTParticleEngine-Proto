# BLTParticleEngine-Proto
Prototype particle system design for use in roguelike game engine.

Todo List:
- [x] Basic Particle Class
- [x] Basic Emitter Class
- [x] Render Loop
- [x] Configurable Delay for Starting System
- [ ] Abstract System Configuration to txt File
- [x] Particle Velocity
- [ ] Radial Acceleration
- [ ] Tangential Acceleration
- [ ] Friction
- [x] Color Particles
- [x] Color/Opacity Change Based On Life Span
- [ ] Emit-Particle Class (extends Particle class with logic for spawning particles)
    (still respects parent Emitter's spawn limits)
- [ ] Figure out how Emitters will Define, Configure, and Update Emit-Particles
- [ ] Figure out way to inject emitters with additional logic for more complex particle effects
- [ ] Config Alias for Continous and One Off Effects
- [ ] Support for Z axis
- [ ] Port to Rust for Production
