<?php

namespace Drupal\pcp_g0_fixture;

/**
 * Normalizes a fixture label without external dependencies.
 *
 * Internal ASCII whitespace is collapsed while other characters are kept.
 */
final class EventLabelNormalizer {

  /**
   * Trims surrounding whitespace and collapses internal ASCII whitespace.
   */
  public function normalize(string $label): string {
    return preg_replace('/[ \t\r\n]+/', ' ', trim($label)) ?? '';
  }

}
