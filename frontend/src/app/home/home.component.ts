import { Router } from '@angular/router' 
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Title } from '@angular/platform-browser';
import { AuthService } from '../auth/auth.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {

  constructor(
    private title: Title,
    private router: Router,
    private authService: AuthService,
  ) {
    this.title.setTitle('Shopping List | Lista de Compras')
  }
}