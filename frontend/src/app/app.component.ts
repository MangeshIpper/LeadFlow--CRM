
import { Component, inject, signal } from '@angular/core';

import { HealthService } from './services/health.service';

@Component({
  selector: 'app-root',
  standalone: true,
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  private readonly healthService = inject(HealthService);

  readonly backendStatus = signal('Not checked');

  checkBackend(): void {
    this.backendStatus.set('Checking...');

    this.healthService.check().subscribe({
      next: (response) => {
        this.backendStatus.set(
          `${response.service}: ${response.status}`
        );
      },
      error: () => {
        this.backendStatus.set('API connection failed');
      }
    });
  }
}
